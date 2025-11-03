"""
Generator endpoints - wrapping existujících Python generátorů.

Tento modul poskytuje REST API pro všech 17 Mausritter generátorů.
MVP fáze: 5 core generátorů (Character, NPC, Hex, Settlement, Weather)
"""

import sys
import dataclasses
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Přidat parent directory do Python path, aby bylo možné importovat src/
backend_dir = Path(__file__).parent.parent.parent
project_root = backend_dir.parent
sys.path.insert(0, str(project_root))

# Import generátorů - MVP (Week 1)
from src.generators.character import CharacterGenerator
from src.generators.npc import NPCGenerator
from src.generators.hex import HexGenerator
from src.generators.settlement import SettlementGenerator
from src.generators.weather import WeatherGenerator

# Import generátorů - V2 (Všech 17)
from src.generators.hireling import HirelingGenerator
from src.generators.reaction import ReactionGenerator
from src.generators.spell import SpellGenerator
from src.generators.treasure import TreasureGenerator
from src.generators.adventure import AdventureSeedGenerator
from src.generators.adventure_hook import AdventureHookGenerator
from src.generators.creature_variant import CreatureVariantGenerator
from src.generators.tavern import TavernGenerator
from src.generators.dungeon import DungeonGenerator
from src.generators.rumor import RumorGenerator
from src.generators.hexcrawl import HexcrawlGenerator

router = APIRouter()

# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class CharacterRequest(BaseModel):
    """Request model pro Character Generator."""
    name: Optional[str] = Field(None, description="Custom jméno (optional)")
    gender: Optional[str] = Field(None, description="Pohlaví: 'male' nebo 'female' (optional)")

class NPCRequest(BaseModel):
    """Request model pro NPC Generator."""
    name: Optional[str] = Field(None, description="Custom jméno (optional)")
    gender: Optional[str] = Field(None, description="Pohlaví: 'male' nebo 'female' (optional)")

class HexRequest(BaseModel):
    """Request model pro Hex Generator."""
    with_settlement: bool = Field(False, description="Vygenerovat settlement pokud je kategorie 1 (optional)")

class SettlementRequest(BaseModel):
    """Request model pro Settlement Generator."""
    with_name: bool = Field(False, description="Vygenerovat jméno osady (optional)")
    no_tavern: bool = Field(False, description="Nevytvářet hospodu ani pro velké osady (optional)")

class WeatherRequest(BaseModel):
    """Request model pro Weather Generator."""
    season: str = Field(..., description="Roční období: 'spring', 'summer', 'autumn', 'winter'")
    with_event: bool = Field(False, description="Zahrnout sezónní událost (optional)")

# V2 Request Models

class HirelingRequest(BaseModel):
    """Request model pro Hireling Generator."""
    type: Optional[int] = Field(None, ge=1, le=9, description="Typ pomocníka (1-9), optional")
    name: Optional[str] = Field(None, description="Custom jméno (optional)")
    gender: Optional[str] = Field(None, description="Pohlaví: 'male' nebo 'female' (optional)")

class ReactionRequest(BaseModel):
    """Request model pro Reaction Roll."""
    modifier: int = Field(0, ge=-6, le=6, description="Modifikátor (-6 až +6)")

class SpellRequest(BaseModel):
    """Request model pro Spell Generator."""
    pass  # Žádné parametry

class TreasureRequest(BaseModel):
    """Request model pro Treasure Generator."""
    bonus: int = Field(0, ge=0, le=4, description="Bonusové hody (0-4)")

class AdventureRequest(BaseModel):
    """Request model pro Adventure Seed Generator."""
    custom: bool = Field(False, description="Custom mode (mix & match ze sloupců)")
    with_inspiration: bool = Field(False, description="Zahrnout inspirační text")

class HookRequest(BaseModel):
    """Request model pro Adventure Hook Generator."""
    pass  # Žádné parametry

class TavernRequest(BaseModel):
    """Request model pro Tavern Generator."""
    pass  # Žádné parametry

class DungeonRequest(BaseModel):
    """Request model pro Dungeon Generator."""
    rooms: int = Field(6, ge=1, le=20, description="Počet místností (1-20)")
    with_settlement: bool = Field(False, description="Force past=20 (Mouse settlement)")

class RumorRequest(BaseModel):
    """Request model pro Rumor Generator."""
    core_only: bool = Field(False, description="Core mode only (bez extended features)")
    advanced: bool = Field(True, description="Advanced mode (více details)")

class HexcrawlRequest(BaseModel):
    """Request model pro Hexcrawl Generator."""
    preset: str = Field("standard", description="Preset: 'standard', 'large', 'small'")
    settlements: Optional[int] = Field(None, description="Počet osad (optional)")
    dungeons: Optional[int] = Field(None, description="Počet dungeonů (optional)")
    factions: Optional[int] = Field(None, description="Počet frakcí (optional)")
    core_only: bool = Field(False, description="Core mode only")

# ============================================================================
# ENDPOINTS - CORE GENERATORS (MVP)
# ============================================================================

@router.post("/character")
async def generate_character(request: CharacterRequest):
    """
    Vygeneruj náhodnou myší postavu.

    **Parametry:**
    - `name` (optional): Custom jméno postavy
    - `gender` (optional): 'male' nebo 'female'

    **Returns:**
    - Kompletní character data (stats, equipment, background, appearance)

    **Příklad:**
    ```json
    {
      "name": "Pepřík Hrabal",
      "background": "Stěnolezec",
      "strength": 8,
      "dexterity": 11,
      "willpower": 12,
      "max_hp": 6,
      ...
    }
    ```
    """
    try:
        character = CharacterGenerator.create(
            name=request.name,
            gender=request.gender
        )
        return CharacterGenerator.to_dict(character)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Character generation failed: {str(e)}")


@router.post("/npc")
async def generate_npc(request: NPCRequest):
    """
    Vygeneruj náhodné NPC (non-player character).

    **Parametry:**
    - `name` (optional): Custom jméno
    - `gender` (optional): 'male' nebo 'female'

    **Returns:**
    - NPC data (jméno, status, vzhled, quirk, touha, vztah)
    """
    try:
        npc = NPCGenerator.create(
            name=request.name,
            gender=request.gender
        )
        return NPCGenerator.to_dict(npc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NPC generation failed: {str(e)}")


@router.post("/hex")
async def generate_hex(request: HexRequest):
    """
    Vygeneruj hex pro hexcrawl mapu.

    **Parametry:**
    - `with_settlement` (optional): Pokud true, vygeneruje settlement pokud kategorie=1

    **Returns:**
    - Hex data (typ, kategorie, detail, háček, optional settlement)
    """
    try:
        if request.with_settlement:
            hex_data = HexGenerator.create_with_settlement()
        else:
            hex_data = HexGenerator.create()
        return HexGenerator.to_dict(hex_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hex generation failed: {str(e)}")


@router.post("/settlement")
async def generate_settlement(request: SettlementRequest):
    """
    Vygeneruj myší osadu (settlement).

    **Parametry:**
    - `with_name` (optional): Pokud true, vygeneruje jméno osady
    - `no_tavern` (optional): Pokud true, nevytvoří hospodu ani pro velké osady

    **Returns:**
    - Settlement data (velikost, vláda, detaily, živnosti, prvky, událost, hospoda)
    """
    try:
        settlement = SettlementGenerator.create(
            no_tavern=request.no_tavern
        )
        return SettlementGenerator.to_dict(settlement)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settlement generation failed: {str(e)}")


@router.post("/weather")
async def generate_weather(request: WeatherRequest):
    """
    Vygeneruj počasí pro dané roční období.

    **Parametry:**
    - `season` (REQUIRED): 'spring', 'summer', 'autumn', nebo 'winter'
    - `with_event` (optional): Pokud true, zahrnuje sezónní událost

    **Returns:**
    - Weather data (roční období, počasí, efekt, optional událost)
    """
    try:
        # Validace season
        valid_seasons = ['spring', 'summer', 'autumn', 'winter']
        if request.season.lower() not in valid_seasons:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid season. Must be one of: {', '.join(valid_seasons)}"
            )

        weather = WeatherGenerator.create(
            season=request.season.lower(),
            with_event=request.with_event
        )
        return WeatherGenerator.to_dict(weather)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather generation failed: {str(e)}")


# ============================================================================
# ENDPOINTS - V2 GENERATORS (ALL 17)
# ============================================================================

@router.post("/hireling")
async def generate_hireling(request: HirelingRequest):
    """
    Vygeneruj pomocníka (hireling).

    **Parametry:**
    - `type` (optional): Typ pomocníka (1-9)
    - `name` (optional): Custom jméno
    - `gender` (optional): 'male' nebo 'female'

    **Returns:**
    - Hireling data včetně availability
    """
    try:
        hireling, availability = HirelingGenerator.create(
            type_id=request.type,
            name=request.name,
            gender=request.gender
        )
        result = HirelingGenerator.to_dict(hireling)
        result["availability"] = availability
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hireling generation failed: {str(e)}")


@router.post("/reaction")
async def generate_reaction(request: ReactionRequest):
    """
    Vygeneruj reaction roll (2d6 + modifier).

    **Parametry:**
    - `modifier` (optional): Modifikátor (-6 až +6), default 0

    **Returns:**
    - Reaction data (roll, total, reaction type, description)
    """
    try:
        reaction = ReactionGenerator.create(modifier=request.modifier)
        return ReactionGenerator.to_dict(reaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reaction generation failed: {str(e)}")


@router.post("/spell")
async def generate_spell(request: SpellRequest):
    """
    Vygeneruj náhodné kouzlo.

    **Parametry:**
    - Žádné

    **Returns:**
    - Spell data (název, efekt, hod)
    """
    try:
        spell = SpellGenerator.create()
        return SpellGenerator.to_dict(spell)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spell generation failed: {str(e)}")


@router.post("/treasure")
async def generate_treasure(request: TreasureRequest):
    """
    Vygeneruj treasure hoard.

    **Parametry:**
    - `bonus` (optional): Bonusové hody (0-4), default 0

    **Returns:**
    - Treasure data (items, total_rolls, bonus_rolls)
    """
    try:
        treasure = TreasureGenerator.create(bonus_rolls=request.bonus)
        return dataclasses.asdict(treasure)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Treasure generation failed: {str(e)}")


@router.post("/adventure")
async def generate_adventure(request: AdventureRequest):
    """
    Vygeneruj adventure seed.

    **Parametry:**
    - `custom` (optional): Custom mode (mix & match), default False
    - `with_inspiration` (optional): Zahrnout inspirační text, default False

    **Returns:**
    - Adventure seed (creature, problem, complication, optional inspiration)
    """
    try:
        if request.custom:
            seed = AdventureSeedGenerator.create_custom()
        else:
            seed = AdventureSeedGenerator.create()

        result = AdventureSeedGenerator.to_dict(seed)
        if request.with_inspiration:
            result["inspiration"] = AdventureSeedGenerator.get_inspiration_text(seed)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Adventure generation failed: {str(e)}")


@router.post("/hook")
async def generate_hook(request: HookRequest):
    """
    Vygeneruj adventure hook.

    **Parametry:**
    - Žádné

    **Returns:**
    - Hook data (hook, category, questions)
    """
    try:
        hook = AdventureHookGenerator.create()
        return AdventureHookGenerator.to_dict(hook)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hook generation failed: {str(e)}")


@router.post("/creature/{creature_type}")
async def generate_creature(creature_type: str):
    """
    Vygeneruj creature variant pro daný typ.

    **Path Parameters:**
    - `creature_type`: ghost | snake | cat | rat | mouse | spider | owl | centipede | fairy | crow | frog

    **Returns:**
    - Creature variant data (type, variant, description, roll)
    """
    try:
        # Validace typu
        valid_types = ['ghost', 'snake', 'cat', 'rat', 'mouse', 'spider', 'owl', 'centipede', 'fairy', 'crow', 'frog']
        if creature_type.lower() not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid creature type. Must be one of: {', '.join(valid_types)}"
            )

        creature = CreatureVariantGenerator.create(creature_type=creature_type.lower())
        return CreatureVariantGenerator.to_dict(creature)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Creature generation failed: {str(e)}")


@router.post("/tavern")
async def generate_tavern(request: TavernRequest):
    """
    Vygeneruj hospodu (tavern).

    **Parametry:**
    - Žádné

    **Returns:**
    - Tavern data (name, specialty)
    """
    try:
        tavern = TavernGenerator.create()
        return TavernGenerator.to_dict(tavern)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tavern generation failed: {str(e)}")


@router.post("/dungeon")
async def generate_dungeon(request: DungeonRequest):
    """
    Vygeneruj dungeon (dobrodružné místo).

    **Parametry:**
    - `rooms` (optional): Počet místností (1-20), default 6
    - `with_settlement` (optional): Force past=20 (Mouse settlement), default False

    **Returns:**
    - Dungeon data (past, decay, inhabitants, goal, secret, rooms, optional settlement)
    """
    try:
        if request.with_settlement:
            dungeon = DungeonGenerator.create_with_settlement(rooms=request.rooms)
        else:
            dungeon = DungeonGenerator.create(rooms=request.rooms)
        return DungeonGenerator.to_dict(dungeon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dungeon generation failed: {str(e)}")


@router.post("/rumor")
async def generate_rumor(request: RumorRequest):
    """
    Vygeneruj zvěsti (rumors).

    **Parametry:**
    - `count` (optional): Počet zvěstí, default 6
    - `category` (optional): Kategorie zvěsti
    - `core_only` (optional): Core mode only, default True

    **Returns:**
    - Rumors data (list of rumors with truthfulness)
    """
    try:
        rumors = RumorGenerator.create(
            core_only=request.core_only,
            advanced=request.advanced
        )
        return {"rumors": [dataclasses.asdict(r) for r in rumors]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rumor generation failed: {str(e)}")


@router.post("/hexcrawl")
async def generate_hexcrawl(request: HexcrawlRequest):
    """
    Vygeneruj celý hexcrawl (bulk generation).

    **Parametry:**
    - `size` (optional): Velikost grid, default 5 (5×5 = 25 hexů)
    - `settlements` (optional): Počet osad, default 3
    - `dungeons` (optional): Počet dungeonů, default 3
    - `rumors` (optional): Počet zvěstí, default 6

    **Returns:**
    - Hexcrawl data (hexes, settlements, dungeons, rumors)
    """
    try:
        hexcrawl = HexcrawlGenerator.create(
            preset=request.preset,
            settlements=request.settlements,
            dungeons=request.dungeons,
            factions=request.factions,
            core_only=request.core_only
        )
        return HexcrawlGenerator.to_dict(hexcrawl)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hexcrawl generation failed: {str(e)}")


# ============================================================================
# STATUS ENDPOINT
# ============================================================================

@router.get("/status")
async def generator_status():
    """
    Vrátí status všech generátorů (které jsou implementované).
    """
    return {
        "total_generators": 17,
        "implemented": 17,
        "status": "✅ All generators implemented!",
        "generators": [
            {"name": "character", "endpoint": "/api/v1/generate/character", "status": "✅"},
            {"name": "npc", "endpoint": "/api/v1/generate/npc", "status": "✅"},
            {"name": "hireling", "endpoint": "/api/v1/generate/hireling", "status": "✅"},
            {"name": "weather", "endpoint": "/api/v1/generate/weather", "status": "✅"},
            {"name": "reaction", "endpoint": "/api/v1/generate/reaction", "status": "✅"},
            {"name": "spell", "endpoint": "/api/v1/generate/spell", "status": "✅"},
            {"name": "treasure", "endpoint": "/api/v1/generate/treasure", "status": "✅"},
            {"name": "adventure", "endpoint": "/api/v1/generate/adventure", "status": "✅"},
            {"name": "hook", "endpoint": "/api/v1/generate/hook", "status": "✅"},
            {"name": "creature", "endpoint": "/api/v1/generate/creature/{type}", "status": "✅"},
            {"name": "tavern", "endpoint": "/api/v1/generate/tavern", "status": "✅"},
            {"name": "settlement", "endpoint": "/api/v1/generate/settlement", "status": "✅"},
            {"name": "hex", "endpoint": "/api/v1/generate/hex", "status": "✅"},
            {"name": "dungeon", "endpoint": "/api/v1/generate/dungeon", "status": "✅"},
            {"name": "rumor", "endpoint": "/api/v1/generate/rumor", "status": "✅"},
            {"name": "hexcrawl", "endpoint": "/api/v1/generate/hexcrawl", "status": "✅"}
        ],
        "creature_types": ["ghost", "snake", "cat", "rat", "mouse", "spider", "owl", "centipede", "fairy", "crow", "frog"]
    }
