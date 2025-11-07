// Campaign State Types for GM Dashboard

export interface Mouse {
  id: string;
  name: string;
  hp: number;
  maxHp: number;
  grit: number;
  maxGrit: number;
  pips: number;
  level: number;
  background?: string;
  disposition?: string;
  birthsign?: string;
  coat?: string;
  inventory?: InventoryItem[];
  conditions?: string[];
  notes?: string;
}

export interface InventoryItem {
  id: string;
  name: string;
  slots: number;
  equipped: boolean;
  description?: string;
}

export interface Creature {
  id: string;
  name: string;
  hp: number;
  attack: string;
  wants: string;
  special?: string[];
  description?: string;
  source: 'rulebook' | 'generated' | 'custom';
}

export interface HexData {
  id: string;
  q: number; // Axial coordinate
  r: number; // Axial coordinate
  terrain: string;
  settlement?: Settlement;
  location?: Location;
  explored: boolean;
  notes?: string;
}

export interface Settlement {
  id: string;
  name: string;
  size: 'hamlet' | 'village' | 'town';
  description?: string;
  npcs?: NPC[];
}

export interface Location {
  id: string;
  name: string;
  type: 'dungeon' | 'ruin' | 'landmark' | 'wilderness';
  description?: string;
}

export interface NPC {
  id: string;
  name: string;
  role: string;
  location: string; // hex id or settlement id
  personality?: string;
  rumors?: Rumor[];
  notes?: string;
}

export interface Rumor {
  id: string;
  text: string;
  truthLevel: 'truth' | 'partial' | 'lie';
  revealed: boolean;
}

export interface WeatherState {
  current: string;
  roll: number;
  season: 'spring' | 'summer' | 'fall' | 'winter';
  effects?: string[];
}

export interface Encounter {
  id: string;
  day: number;
  watch: 'morning' | 'afternoon' | 'evening' | 'night';
  hexId?: string;
  creature: string;
  reaction?: string;
  outcome?: string;
  active: boolean;
}

export interface DiceRoll {
  id: string;
  timestamp: Date;
  type: string; // 'd6', '2d6', 'd20', etc.
  result: number | number[];
  roller: 'gm' | 'player';
  context?: string;
}

export interface CanvasState {
  id: string;
  name: string;
  drawingData?: string; // Base64 PNG of canvas
  uploadedImage?: string; // Base64 of uploaded image
  timestamp: Date;
}

export interface CampaignState {
  id: string;
  name: string;
  created: Date;
  lastModified: Date;

  // Time tracking
  currentDay: number;
  currentWatch: 'morning' | 'afternoon' | 'evening' | 'night';

  // Party
  party: Mouse[];

  // World
  hexMap: HexData[];
  settlements: Settlement[];
  npcs: NPC[];

  // Weather & Encounters
  weather: WeatherState;
  encounters: Encounter[];

  // Bestiary
  bestiary: Creature[];

  // Tactical Maps
  tacticalMaps: {
    current: CanvasState | null;
    saved: CanvasState[];
  };

  // History & Logs
  weatherLog: WeatherState[];
  rollHistory: DiceRoll[];

  // Notes
  gmNotes: string;
  sessionLog: string[];
}

// Helper function to create empty campaign
export function createEmptyCampaign(name: string = "New Campaign"): CampaignState {
  return {
    id: crypto.randomUUID(),
    name,
    created: new Date(),
    lastModified: new Date(),
    currentDay: 1,
    currentWatch: 'morning',
    party: [],
    hexMap: [],
    settlements: [],
    npcs: [],
    weather: {
      current: 'Normal',
      roll: 7,
      season: 'spring',
    },
    encounters: [],
    bestiary: [],
    tacticalMaps: {
      current: null,
      saved: [],
    },
    weatherLog: [],
    rollHistory: [],
    gmNotes: '',
    sessionLog: [],
  };
}

// Mock data for testing
export function createMockCampaign(): CampaignState {
  const campaign = createEmptyCampaign("Thornwood Vale");

  // Add 4 test mice
  campaign.party = [
    {
      id: '1',
      name: 'Pip',
      hp: 4,
      maxHp: 6,
      grit: 2,
      maxGrit: 3,
      pips: 150,
      level: 1,
      background: 'Street Tough',
      conditions: [],
    },
    {
      id: '2',
      name: 'Rosa',
      hp: 5,
      maxHp: 5,
      grit: 3,
      maxGrit: 3,
      pips: 200,
      level: 2,
      background: 'Wise Wanderer',
      conditions: [],
    },
    {
      id: '3',
      name: 'Max',
      hp: 3,
      maxHp: 4,
      grit: 1,
      maxGrit: 2,
      pips: 80,
      level: 1,
      background: 'Tinker',
      conditions: ['Exhausted'],
    },
    {
      id: '4',
      name: 'Lily',
      hp: 6,
      maxHp: 6,
      grit: 2,
      maxGrit: 2,
      pips: 120,
      level: 1,
      background: 'Kitchen Keeper',
      conditions: [],
    },
  ];

  return campaign;
}
