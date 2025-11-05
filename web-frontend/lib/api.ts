/**
 * API Client pro Mausritter Backend
 *
 * Obsahuje TypeScript types a fetch wrappery pro všech 17 generátorů.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// ============================================================================
// TypeScript Types - Request Models
// ============================================================================

export interface CharacterRequest {
  name?: string;
  gender?: 'male' | 'female';
}

export interface NPCRequest {
  name?: string;
  gender?: 'male' | 'female';
}

export interface HexRequest {
  with_settlement?: boolean;
}

export interface SettlementRequest {
  with_name?: boolean;
  no_tavern?: boolean;
}

export interface WeatherRequest {
  season: 'spring' | 'summer' | 'autumn' | 'winter';
  with_event?: boolean;
}

export interface HirelingRequest {
  type?: number; // 1-9
  name?: string;
  gender?: 'male' | 'female';
}

export interface ReactionRequest {
  modifier?: number; // -6 to +6
}

export interface SpellRequest {}

export interface TreasureRequest {
  bonus?: number; // 0-4
}

export interface AdventureRequest {
  custom?: boolean;
  with_inspiration?: boolean;
}

export interface HookRequest {}

export interface TavernRequest {}

export interface DungeonRequest {
  rooms?: number; // 1-20
  with_settlement?: boolean;
}

export interface RumorRequest {
  core_only?: boolean;
  advanced?: boolean;
}

export interface HexcrawlRequest {
  preset?: 'standard' | 'large' | 'small';
  settlements?: number;
  dungeons?: number;
  factions?: number;
  core_only?: boolean;
}

export interface CreatureRequest {
  type: 'ghost' | 'snake' | 'cat' | 'rat' | 'mouse' | 'spider' | 'owl' | 'centipede' | 'fairy' | 'crow' | 'frog';
}

// ============================================================================
// TypeScript Types - Response Models
// ============================================================================

export interface CharacterResponse {
  name: string;
  background: string;
  strength: number;
  dexterity: number;
  willpower: number;
  max_hp: number;
  current_hp: number;
  inventory: (string | null)[];
  appearance: string;
  personality: string | null;
  disposition: string | null;
  birthsign: string;
  coat: string;
  conditions: string[];
  level: number;
  experience: number;
  notes: string;
}

export interface NPCResponse {
  name: string;
  gender: string;
  social_status: string;
  birthsign: string;
  appearance: string;
  quirk: string;
  desire: string;
  relationship: string;
  reaction: string;
  roll_social_status: number;
  roll_birthsign: number;
  roll_appearance: number;
  roll_quirk: number;
  roll_desire: number;
  roll_relationship: number;
  roll_reaction: number;
}

export interface HexResponse {
  type: string;
  type_roll: number;
  type_emoji: string;
  detail: {
    category: number;
    category_name: string;
    subtype: number;
    name: string;
    hook: string;
  };
  description: string;
  is_settlement: boolean;
}

export interface SettlementResponse {
  size: {
    name: string;
    population: string;
    value: number;
  };
  government: string;
  detail: string;
  trades: string[];
  features: string[];
  event: string;
  name?: string;
  tavern?: {
    name: string;
    specialty: string;
  };
  rolls?: {
    size_die1: number;
    size_die2: number;
    government: number;
    detail: number;
    trades: number[];
    features: number[];
    event: number;
  };
}

export interface WeatherResponse {
  season: string;
  weather: string;
  unfavorable: boolean;
  event: string | null;
  notes: string;
}

export interface HirelingResponse {
  name: string;
  type: string;
  daily_wage: number;
  hp: number;
  strength: number;
  dexterity: number;
  willpower: number;
  inventory: (string | null)[];
  level: number;
  experience: number;
  morale: string;
  notes: string;
  availability: number;
}

export interface ReactionResponse {
  roll: number;
  reaction: string;
  question: string;
  notes: string;
}

export interface SpellResponse {
  roll: number;
  name: string;
  effect: string;
  recharge: string;
  tags: string[];
  notes: string;
}

export interface TreasureResponse {
  items: Array<{
    type: string;
    name: string;
    description: string;
    value: number | null;
    slots: number;
    usage_dots: number;
    spell: any | null;
    magic_sword: any | null;
    tool: any | null;
    armor: any | null;
    buyer: any | null;
    quantity: number;
    notes: string;
  }>;
  total_value: number;
  bonus_rolls: number;
  total_rolls: number;
  notes: string;
}

export interface AdventureResponse {
  roll: number;
  creature: string;
  problem: string;
  complication: string;
  notes: string;
}

export interface HookResponse {
  hook: string;
  category: string;
  category_name: string;
  questions: string[];
  roll: number;
}

export interface TavernResponse {
  name_part1: string;
  name_part2: string;
  full_name: string;
  specialty: string;
  roll_part1: number;
  roll_part2: number;
  roll_specialty: number;
}

export interface DungeonResponse {
  past: { roll: number; name: string };
  decay: { roll: number; name: string };
  inhabitants: { roll: number; name: string };
  goal: { roll: number; name: string };
  secret: { roll: number; name: string };
  room_count: number;
  rooms: Array<{
    number: number;
    type: { roll: number; name: string; emoji: string };
    has_creature: boolean;
    has_treasure: boolean;
    feature: { roll: number; name: string };
  }>;
  has_settlement: boolean;
  description: string;
}

export interface RumorResponse {
  rumors: Array<{
    rumor: string;
    truthfulness: string;
    roll: number;
  }>;
}

export interface HexcrawlSettlement {
  size_name: string;
  population: string;
  size_value: number;
  government: string;
  detail: string;
  trades: string[];
  features: string[];
  event: string;
  name: string;
  tavern: {
    name_part1: string;
    name_part2: string;
    full_name: string;
    specialty: string;
  } | null;
  is_friendly: boolean;
}

export interface HexcrawlDungeon {
  past: string;
  past_roll: number;
  decay: string;
  decay_roll: number;
  inhabitants: string;
  inhabitants_roll: number;
  goal: string;
  goal_roll: number;
  secret: string;
  secret_roll: number;
  rooms: Array<{
    room_number: number;
    room_type: string;
    room_type_roll: number;
    has_creature: boolean;
    has_treasure: boolean;
    feature: string;
    feature_roll: number;
  }>;
  settlement: any | null;
  description: string;
}

export interface HexcrawlHex {
  type: string;
  type_roll: number;
  detail_category: number;
  detail_subtype: number | null;
  detail_name: string;
  detail_hook: string;
  settlement: HexcrawlSettlement | null;
  description: string;
}

export interface HexcrawlResponse {
  hexes: HexcrawlHex[];
  settlements: HexcrawlSettlement[];
  dungeons: HexcrawlDungeon[];
  rumors: any[];
  metadata: {
    preset: string;
    total_hexes: number;
    total_settlements: number;
    total_dungeons: number;
  };
}

export interface CreatureResponse {
  creature_type: string;
  variant: string;
  description: string;
  roll: number;
}

export interface GeneratorStatus {
  total_generators: number;
  implemented: number;
  status: string;
  generators: Array<{
    name: string;
    endpoint: string;
    status: string;
  }>;
  creature_types?: string[];
}

// ============================================================================
// API Error Handling
// ============================================================================

export class APIError extends Error {
  constructor(public status: number, message: string, public details?: any) {
    super(message);
    this.name = 'APIError';
  }
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        response.status,
        errorData.detail || `Request failed with status ${response.status}`,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(0, `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// ============================================================================
// API Functions - Generator Endpoints
// ============================================================================

export async function generateCharacter(request: CharacterRequest = {}): Promise<CharacterResponse> {
  return fetchAPI('/api/v1/generate/character', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateNPC(request: NPCRequest = {}): Promise<NPCResponse> {
  return fetchAPI('/api/v1/generate/npc', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateHex(request: HexRequest = {}): Promise<HexResponse> {
  return fetchAPI('/api/v1/generate/hex', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateSettlement(request: SettlementRequest = {}): Promise<SettlementResponse> {
  return fetchAPI('/api/v1/generate/settlement', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateWeather(request: WeatherRequest): Promise<WeatherResponse> {
  return fetchAPI('/api/v1/generate/weather', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateHireling(request: HirelingRequest = {}): Promise<HirelingResponse> {
  return fetchAPI('/api/v1/generate/hireling', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateReaction(request: ReactionRequest = {}): Promise<ReactionResponse> {
  return fetchAPI('/api/v1/generate/reaction', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateSpell(request: SpellRequest = {}): Promise<SpellResponse> {
  return fetchAPI('/api/v1/generate/spell', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateTreasure(request: TreasureRequest = {}): Promise<TreasureResponse> {
  return fetchAPI('/api/v1/generate/treasure', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateAdventure(request: AdventureRequest = {}): Promise<AdventureResponse> {
  return fetchAPI('/api/v1/generate/adventure', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateHook(request: HookRequest = {}): Promise<HookResponse> {
  return fetchAPI('/api/v1/generate/hook', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateTavern(request: TavernRequest = {}): Promise<TavernResponse> {
  return fetchAPI('/api/v1/generate/tavern', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateDungeon(request: DungeonRequest = {}): Promise<DungeonResponse> {
  return fetchAPI('/api/v1/generate/dungeon', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateRumor(request: RumorRequest = {}): Promise<RumorResponse> {
  return fetchAPI('/api/v1/generate/rumor', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateHexcrawl(request: HexcrawlRequest = {}): Promise<HexcrawlResponse> {
  return fetchAPI('/api/v1/generate/hexcrawl', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function generateCreature(type: CreatureRequest['type']): Promise<CreatureResponse> {
  return fetchAPI(`/api/v1/generate/creature/${type}`, {
    method: 'POST',
  });
}

// ============================================================================
// Utility Endpoints
// ============================================================================

export async function getGeneratorStatus(): Promise<GeneratorStatus> {
  return fetchAPI('/api/v1/generate/status');
}

export async function healthCheck(): Promise<{ status: string; message: string }> {
  return fetchAPI('/health');
}
