"""
Generator endpoints - wrapping existujících Python generátorů.

Tento modul poskytuje REST API pro všech 17 Mausritter generátorů.
MVP fáze: 5 core generátorů (Character, NPC, Hex, Settlement, Weather)
"""

import sys
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Přidat parent directory do Python path, aby bylo možné importovat src/
backend_dir = Path(__file__).parent.parent.parent
project_root = backend_dir.parent
sys.path.insert(0, str(project_root))

# Import generátorů
from src.generators.character import CharacterGenerator
from src.generators.npc import NPCGenerator
from src.generators.hex import HexGenerator
from src.generators.settlement import SettlementGenerator
from src.generators.weather import WeatherGenerator

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
# PLACEHOLDER ENDPOINTS - V2 PHASE
# ============================================================================
# TODO: Implementovat ve V2 (zbývajících 12 generátorů)
# - Hireling, Reaction, Spell, Treasure, Adventure Seed, Adventure Hook
# - Creature Variant, Tavern, Dungeon, Rumor, Hexcrawl (bulk)

@router.get("/status")
async def generator_status():
    """
    Vrátí status všech generátorů (které jsou implementované).
    """
    return {
        "total_generators": 17,
        "implemented": 5,
        "mvp_generators": [
            "character",
            "npc",
            "hex",
            "settlement",
            "weather"
        ],
        "v2_generators": [
            "hireling",
            "reaction",
            "spell",
            "treasure",
            "adventure",
            "hook",
            "creature",
            "tavern",
            "dungeon",
            "rumor",
            "hexcrawl"
        ]
    }
