-- ============================================================================
-- MAUSRITTER WEB PLATFORM - DATABASE SCHEMA
-- ============================================================================
-- Version: 1.0
-- Date: 2025-11-03
-- Database: PostgreSQL 15 (Supabase)
--
-- Purpose: Complete database schema for Mausritter web platform
-- Tables: 12 total (users via Supabase Auth, 11 custom)
-- Security: Row Level Security (RLS) enabled on all tables
-- ============================================================================

-- Note: Run this in Supabase SQL Editor
-- Prerequisites: Supabase project created, Auth enabled

-- ============================================================================
-- EXTENSIONS
-- ============================================================================

-- UUID generation (usually pre-installed in Supabase)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TABLE 1: PROFILES
-- ============================================================================
-- Purpose: User profile data (extends Supabase auth.users)
-- Relationship: 1-to-1 with auth.users
-- RLS: Public read, user update own profile

CREATE TABLE profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username text UNIQUE NOT NULL,
  role text NOT NULL CHECK (role IN ('gm', 'player')),
  avatar_url text,
  bio text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  CONSTRAINT username_length CHECK (char_length(username) >= 3 AND char_length(username) <= 20),
  CONSTRAINT username_format CHECK (username ~ '^[a-zA-Z0-9_-]+$')
);

-- Indexes
CREATE INDEX idx_profiles_username ON profiles(username);
CREATE INDEX idx_profiles_role ON profiles(role);

-- RLS Policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Trigger: Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 2: CAMPAIGNS
-- ============================================================================
-- Purpose: GM campaigns (sandbox hexcrawl worlds)
-- Relationship: Many campaigns per GM (user)
-- RLS: GM owns campaigns, players can view if member

CREATE TABLE campaigns (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  gm_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Campaign metadata
  name text NOT NULL,
  description text,

  -- World state
  current_season text CHECK (current_season IN ('spring', 'summer', 'autumn', 'winter')),
  current_weather jsonb, -- Weather object from WeatherGenerator
  current_date text, -- In-game date (e.g., "Day 15 of Autumn")

  -- Settings
  is_active boolean DEFAULT true,
  is_public boolean DEFAULT false, -- Can others view/join?

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  last_session_at timestamptz,

  CONSTRAINT campaign_name_length CHECK (char_length(name) >= 3 AND char_length(name) <= 100)
);

-- Indexes
CREATE INDEX idx_campaigns_gm ON campaigns(gm_id);
CREATE INDEX idx_campaigns_active ON campaigns(is_active) WHERE is_active = true;
CREATE INDEX idx_campaigns_public ON campaigns(is_public) WHERE is_public = true;

-- RLS Policies
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD their own campaigns"
  ON campaigns
  USING (auth.uid() = gm_id);

CREATE POLICY "Players can view campaigns they're in"
  ON campaigns FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = id AND cp.player_id = auth.uid()
    )
  );

CREATE POLICY "Anyone can view public campaigns"
  ON campaigns FOR SELECT
  USING (is_public = true);

-- Trigger
CREATE TRIGGER update_campaigns_updated_at
  BEFORE UPDATE ON campaigns
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 3: CAMPAIGN_PLAYERS
-- ============================================================================
-- Purpose: Join table - which players are in which campaigns
-- Relationship: Many-to-many (campaigns <-> players)
-- RLS: GM can manage, players can view

CREATE TABLE campaign_players (
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  player_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Metadata
  joined_at timestamptz DEFAULT now(),
  status text DEFAULT 'active' CHECK (status IN ('active', 'invited', 'inactive')),
  notes text, -- GM notes about this player

  PRIMARY KEY (campaign_id, player_id)
);

-- Indexes
CREATE INDEX idx_campaign_players_campaign ON campaign_players(campaign_id);
CREATE INDEX idx_campaign_players_player ON campaign_players(player_id);

-- RLS Policies
ALTER TABLE campaign_players ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can manage players in their campaigns"
  ON campaign_players
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view their campaign memberships"
  ON campaign_players FOR SELECT
  USING (auth.uid() = player_id);

-- ============================================================================
-- TABLE 4: CHARACTERS
-- ============================================================================
-- Purpose: Player characters (from CharacterGenerator)
-- Relationship: Belongs to campaign and player
-- RLS: Player owns, GM can view

CREATE TABLE characters (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  player_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Character identity
  name text NOT NULL,
  background text NOT NULL, -- e.g., "Stěnolezec"

  -- Attributes
  strength int NOT NULL CHECK (strength >= 1 AND strength <= 18),
  dexterity int NOT NULL CHECK (dexterity >= 1 AND dexterity <= 18),
  willpower int NOT NULL CHECK (willpower >= 1 AND willpower <= 18),

  -- Health
  max_hp int NOT NULL CHECK (max_hp >= 1 AND max_hp <= 6),
  current_hp int NOT NULL CHECK (current_hp >= 0),

  -- Progression
  level int DEFAULT 1 CHECK (level >= 1),
  xp int DEFAULT 0 CHECK (xp >= 0),
  pips int DEFAULT 0 CHECK (pips >= 0 AND pips <= 6),

  -- Wealth
  pence int DEFAULT 0 CHECK (pence >= 0),

  -- Appearance
  birthsign text,
  coat_color text,
  coat_pattern text,
  distinctive_trait text,

  -- Equipment (JSON array of items)
  inventory jsonb DEFAULT '[]'::jsonb,

  -- Conditions
  conditions jsonb DEFAULT '[]'::jsonb, -- ["injured", "exhausted", etc.]

  -- Full snapshot from generator (for reference)
  generated_data jsonb NOT NULL,

  -- Status
  is_alive boolean DEFAULT true,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  CONSTRAINT character_name_length CHECK (char_length(name) >= 1 AND char_length(name) <= 50),
  CONSTRAINT current_hp_max CHECK (current_hp <= max_hp)
);

-- Indexes
CREATE INDEX idx_characters_campaign ON characters(campaign_id);
CREATE INDEX idx_characters_player ON characters(player_id);
CREATE INDEX idx_characters_alive ON characters(is_alive) WHERE is_alive = true;

-- RLS Policies
ALTER TABLE characters ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Players can CRUD their own characters"
  ON characters
  USING (auth.uid() = player_id);

CREATE POLICY "GMs can view all characters in their campaigns"
  ON characters FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Campaign members can view characters"
  ON characters FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = characters.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_characters_updated_at
  BEFORE UPDATE ON characters
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 5: HEXES
-- ============================================================================
-- Purpose: Hexcrawl tiles (5x5 grid per campaign)
-- Relationship: Belongs to campaign
-- RLS: GM manages, players view discovered

CREATE TABLE hexes (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,

  -- Grid position (0-4 for 5x5 grid)
  col int NOT NULL CHECK (col >= 0 AND col <= 4),
  row int NOT NULL CHECK (row >= 0 AND row <= 4),

  -- Hex data (from HexGenerator)
  hex_type text NOT NULL, -- "Otevřená krajina", "Les", "Řeka", "Lidské město"
  category text, -- "Myší osada", "Civilizace", "Zvířata", etc.
  detail text,
  hook text,

  -- Discovery state
  is_discovered boolean DEFAULT false,
  discovered_at timestamptz,
  discovered_by uuid REFERENCES auth.users(id), -- Which player discovered it

  -- GM notes
  notes text,

  -- Full snapshot from generator
  generated_data jsonb NOT NULL,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  UNIQUE (campaign_id, col, row)
);

-- Indexes
CREATE INDEX idx_hexes_campaign ON hexes(campaign_id);
CREATE INDEX idx_hexes_grid ON hexes(campaign_id, col, row);
CREATE INDEX idx_hexes_discovered ON hexes(campaign_id, is_discovered);

-- RLS Policies
ALTER TABLE hexes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD hexes in their campaigns"
  ON hexes
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view discovered hexes"
  ON hexes FOR SELECT
  USING (
    is_discovered = true AND
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = hexes.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_hexes_updated_at
  BEFORE UPDATE ON hexes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 6: SETTLEMENTS
-- ============================================================================
-- Purpose: Mouse settlements (from SettlementGenerator)
-- Relationship: Belongs to hex and campaign
-- RLS: GM manages, players view discovered

CREATE TABLE settlements (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  hex_id uuid REFERENCES hexes(id) ON DELETE CASCADE,

  -- Settlement data
  name text NOT NULL,
  size text NOT NULL, -- "Farma", "Víska", "Město", etc.
  government text, -- "Rada starších", "Šlechtic", etc.
  detail text,
  event text,

  -- Arrays stored as JSONB
  trades jsonb, -- Array of trade strings
  features jsonb, -- Array of feature strings
  tavern jsonb, -- Tavern object (optional)

  -- Discovery state
  is_discovered boolean DEFAULT false,
  discovered_at timestamptz,

  -- Relationship state
  attitude text DEFAULT 'neutral' CHECK (attitude IN ('hostile', 'unfriendly', 'neutral', 'friendly', 'allied')),

  -- GM notes
  notes text,

  -- Full snapshot
  generated_data jsonb NOT NULL,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  CONSTRAINT settlement_name_length CHECK (char_length(name) >= 1 AND char_length(name) <= 100)
);

-- Indexes
CREATE INDEX idx_settlements_campaign ON settlements(campaign_id);
CREATE INDEX idx_settlements_hex ON settlements(hex_id);
CREATE INDEX idx_settlements_discovered ON settlements(campaign_id, is_discovered);

-- RLS Policies
ALTER TABLE settlements ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD settlements in their campaigns"
  ON settlements
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view discovered settlements"
  ON settlements FOR SELECT
  USING (
    is_discovered = true AND
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = settlements.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_settlements_updated_at
  BEFORE UPDATE ON settlements
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 7: DUNGEONS
-- ============================================================================
-- Purpose: Adventure sites (from DungeonGenerator)
-- Relationship: Belongs to hex and campaign
-- RLS: GM manages, players view discovered

CREATE TABLE dungeons (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  hex_id uuid REFERENCES hexes(id) ON DELETE CASCADE,

  -- Dungeon data
  name text NOT NULL,
  past text, -- "Chrám", "Věž", etc.
  decay text, -- "Zatopení", "Magie", etc.
  inhabitants text, -- "Duchové", "Krysy", etc.
  goal text,
  secret text,

  -- Rooms (array of Room objects)
  rooms jsonb NOT NULL, -- [{type, hasCreature, hasTreasure, feature}, ...]

  -- Progress tracking
  is_discovered boolean DEFAULT false,
  discovered_at timestamptz,
  is_cleared boolean DEFAULT false,
  cleared_at timestamptz,
  rooms_explored jsonb DEFAULT '[]'::jsonb, -- Array of room indices explored

  -- GM notes
  notes text,

  -- Full snapshot
  generated_data jsonb NOT NULL,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  CONSTRAINT dungeon_name_length CHECK (char_length(name) >= 1 AND char_length(name) <= 100)
);

-- Indexes
CREATE INDEX idx_dungeons_campaign ON dungeons(campaign_id);
CREATE INDEX idx_dungeons_hex ON dungeons(hex_id);
CREATE INDEX idx_dungeons_discovered ON dungeons(campaign_id, is_discovered);
CREATE INDEX idx_dungeons_cleared ON dungeons(campaign_id, is_cleared);

-- RLS Policies
ALTER TABLE dungeons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD dungeons in their campaigns"
  ON dungeons
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view discovered dungeons"
  ON dungeons FOR SELECT
  USING (
    is_discovered = true AND
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = dungeons.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_dungeons_updated_at
  BEFORE UPDATE ON dungeons
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 8: NPCS
-- ============================================================================
-- Purpose: Non-player characters (from NPCGenerator)
-- Relationship: Belongs to campaign, optionally hex/settlement
-- RLS: GM manages, players view discovered

CREATE TABLE npcs (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
  created_by_gm uuid NOT NULL REFERENCES auth.users(id),

  -- NPC data
  name text NOT NULL,
  social_status text,
  birthsign text,
  appearance text,
  quirk text,
  desire text,
  relationship text, -- To party

  -- Location (optional)
  hex_id uuid REFERENCES hexes(id) ON DELETE SET NULL,
  settlement_id uuid REFERENCES settlements(id) ON DELETE SET NULL,
  dungeon_id uuid REFERENCES dungeons(id) ON DELETE SET NULL,

  -- Discovery state
  is_discovered boolean DEFAULT false,
  discovered_at timestamptz,

  -- Interaction tracking
  last_reaction text, -- Last reaction roll result
  interactions jsonb DEFAULT '[]'::jsonb, -- Array of {date, summary, reaction}

  -- GM notes
  notes text,

  -- Full snapshot
  generated_data jsonb NOT NULL,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  CONSTRAINT npc_name_length CHECK (char_length(name) >= 1 AND char_length(name) <= 50)
);

-- Indexes
CREATE INDEX idx_npcs_campaign ON npcs(campaign_id);
CREATE INDEX idx_npcs_hex ON npcs(hex_id);
CREATE INDEX idx_npcs_settlement ON npcs(settlement_id);
CREATE INDEX idx_npcs_discovered ON npcs(campaign_id, is_discovered);

-- RLS Policies
ALTER TABLE npcs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD NPCs in their campaigns"
  ON npcs
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view discovered NPCs"
  ON npcs FOR SELECT
  USING (
    is_discovered = true AND
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = npcs.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_npcs_updated_at
  BEFORE UPDATE ON npcs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 9: RUMORS
-- ============================================================================
-- Purpose: Rumors (from RumorGenerator)
-- Relationship: Belongs to campaign, links to world entities
-- RLS: GM manages, players view heard rumors

CREATE TABLE rumors (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,

  -- Rumor data
  rumor_text text NOT NULL,
  category text CHECK (category IN ('threat', 'npc', 'location', 'treasure', 'mystery')),
  truthfulness text CHECK (truthfulness IN ('true', 'partial', 'false')),

  -- World connections (optional)
  related_npc_id uuid REFERENCES npcs(id) ON DELETE SET NULL,
  related_hex_id uuid REFERENCES hexes(id) ON DELETE SET NULL,
  related_dungeon_id uuid REFERENCES dungeons(id) ON DELETE SET NULL,
  related_settlement_id uuid REFERENCES settlements(id) ON DELETE SET NULL,

  -- Discovery state
  is_heard boolean DEFAULT false,
  heard_at timestamptz,
  heard_by jsonb DEFAULT '[]'::jsonb, -- Array of player user IDs

  -- Investigation tracking
  is_investigated boolean DEFAULT false,
  truth_revealed boolean DEFAULT false,

  -- GM notes
  notes text,

  -- Full snapshot
  generated_data jsonb NOT NULL,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Indexes
CREATE INDEX idx_rumors_campaign ON rumors(campaign_id);
CREATE INDEX idx_rumors_heard ON rumors(campaign_id, is_heard);
CREATE INDEX idx_rumors_category ON rumors(category);

-- RLS Policies
ALTER TABLE rumors ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD rumors in their campaigns"
  ON rumors
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view heard rumors"
  ON rumors FOR SELECT
  USING (
    is_heard = true AND
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = rumors.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_rumors_updated_at
  BEFORE UPDATE ON rumors
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 10: SESSIONS
-- ============================================================================
-- Purpose: Game session tracking
-- Relationship: Belongs to campaign
-- RLS: GM manages, players view

CREATE TABLE sessions (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,

  -- Session metadata
  session_number int NOT NULL,
  session_date date NOT NULL,
  duration_minutes int, -- Actual play time

  -- Content
  title text,
  summary text,
  notes text,
  highlights jsonb DEFAULT '[]'::jsonb, -- Notable moments

  -- Participants
  players_present jsonb, -- Array of user IDs

  -- In-game tracking
  hexes_explored jsonb DEFAULT '[]'::jsonb, -- Array of hex IDs
  npcs_met jsonb DEFAULT '[]'::jsonb, -- Array of NPC IDs
  combat_encounters int DEFAULT 0,
  treasure_found jsonb DEFAULT '[]'::jsonb,

  -- XP and rewards
  xp_awarded int DEFAULT 0,

  -- Timestamps
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),

  UNIQUE (campaign_id, session_number)
);

-- Indexes
CREATE INDEX idx_sessions_campaign ON sessions(campaign_id);
CREATE INDEX idx_sessions_date ON sessions(session_date DESC);

-- RLS Policies
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "GMs can CRUD sessions in their campaigns"
  ON sessions
  USING (
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
  );

CREATE POLICY "Players can view sessions in their campaigns"
  ON sessions FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = sessions.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- Trigger
CREATE TRIGGER update_sessions_updated_at
  BEFORE UPDATE ON sessions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TABLE 11: DICE_ROLLS
-- ============================================================================
-- Purpose: Dice roll history (optional, pro statistics)
-- Relationship: Belongs to campaign and session
-- RLS: Campaign members can view

CREATE TABLE dice_rolls (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  campaign_id uuid REFERENCES campaigns(id) ON DELETE CASCADE,
  session_id uuid REFERENCES sessions(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES auth.users(id),

  -- Roll data
  dice_type text NOT NULL, -- 'd6', 'd20', '2d6', 'd66', etc.
  result int NOT NULL,
  reason text, -- 'STR test', 'Damage roll', 'Reaction', etc.

  -- Context
  character_id uuid REFERENCES characters(id) ON DELETE SET NULL,

  -- Timestamp
  created_at timestamptz DEFAULT now()
);

-- Indexes
CREATE INDEX idx_dice_rolls_campaign ON dice_rolls(campaign_id);
CREATE INDEX idx_dice_rolls_session ON dice_rolls(session_id);
CREATE INDEX idx_dice_rolls_user ON dice_rolls(user_id);
CREATE INDEX idx_dice_rolls_created ON dice_rolls(created_at DESC);

-- RLS Policies
ALTER TABLE dice_rolls ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Campaign members can insert dice rolls"
  ON dice_rolls FOR INSERT
  WITH CHECK (
    auth.uid() = user_id AND
    (
      -- GM of campaign
      EXISTS (
        SELECT 1 FROM campaigns c
        WHERE c.id = campaign_id AND c.gm_id = auth.uid()
      )
      OR
      -- Player in campaign
      EXISTS (
        SELECT 1 FROM campaign_players cp
        WHERE cp.campaign_id = dice_rolls.campaign_id AND cp.player_id = auth.uid()
      )
    )
  );

CREATE POLICY "Campaign members can view dice rolls"
  ON dice_rolls FOR SELECT
  USING (
    -- GM of campaign
    EXISTS (
      SELECT 1 FROM campaigns c
      WHERE c.id = campaign_id AND c.gm_id = auth.uid()
    )
    OR
    -- Player in campaign
    EXISTS (
      SELECT 1 FROM campaign_players cp
      WHERE cp.campaign_id = dice_rolls.campaign_id AND cp.player_id = auth.uid()
    )
  );

-- ============================================================================
-- UTILITY VIEWS
-- ============================================================================

-- View: Campaign summary statistics
CREATE OR REPLACE VIEW campaign_stats AS
SELECT
  c.id AS campaign_id,
  c.name AS campaign_name,
  c.gm_id,
  COUNT(DISTINCT cp.player_id) AS player_count,
  COUNT(DISTINCT ch.id) AS character_count,
  COUNT(DISTINCT h.id) FILTER (WHERE h.is_discovered = true) AS hexes_discovered,
  COUNT(DISTINCT s.id) FILTER (WHERE s.is_discovered = true) AS settlements_discovered,
  COUNT(DISTINCT d.id) FILTER (WHERE d.is_discovered = true) AS dungeons_discovered,
  COUNT(DISTINCT d.id) FILTER (WHERE d.is_cleared = true) AS dungeons_cleared,
  COUNT(DISTINCT n.id) FILTER (WHERE n.is_discovered = true) AS npcs_met,
  COUNT(DISTINCT sess.id) AS sessions_played,
  MAX(sess.session_date) AS last_session_date
FROM campaigns c
LEFT JOIN campaign_players cp ON c.id = cp.campaign_id
LEFT JOIN characters ch ON c.id = ch.campaign_id
LEFT JOIN hexes h ON c.id = h.campaign_id
LEFT JOIN settlements s ON c.id = s.campaign_id
LEFT JOIN dungeons d ON c.id = d.campaign_id
LEFT JOIN npcs n ON c.id = n.campaign_id
LEFT JOIN sessions sess ON c.id = sess.campaign_id
GROUP BY c.id, c.name, c.gm_id;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Mark hex and its contents as discovered
CREATE OR REPLACE FUNCTION discover_hex(
  p_hex_id uuid,
  p_discovered_by uuid
)
RETURNS void AS $$
BEGIN
  -- Update hex
  UPDATE hexes
  SET
    is_discovered = true,
    discovered_at = now(),
    discovered_by = p_discovered_by
  WHERE id = p_hex_id;

  -- Update settlements in hex
  UPDATE settlements
  SET
    is_discovered = true,
    discovered_at = now()
  WHERE hex_id = p_hex_id;

  -- Update dungeons in hex
  UPDATE dungeons
  SET
    is_discovered = true,
    discovered_at = now()
  WHERE hex_id = p_hex_id;

  -- Update NPCs in hex
  UPDATE npcs
  SET
    is_discovered = true,
    discovered_at = now()
  WHERE hex_id = p_hex_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Note: Initial data (seasons, default values) can be inserted here
-- For now, applications handle this via API

-- ============================================================================
-- GRANTS
-- ============================================================================

-- Supabase handles authentication and RLS automatically
-- No additional grants needed for authenticated users

-- For anon (unauthenticated) access:
-- GRANT SELECT ON profiles TO anon; -- If you want public profiles

-- ============================================================================
-- NOTES
-- ============================================================================

-- To apply this schema:
-- 1. Copy entire file
-- 2. Go to Supabase Dashboard → SQL Editor
-- 3. Paste and run
-- 4. Verify in Table Editor

-- To reset database (CAREFUL - deletes all data):
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;
-- GRANT ALL ON SCHEMA public TO postgres;
-- GRANT ALL ON SCHEMA public TO public;
-- Then re-run this file

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
