"""
Datové modely pro Mausritter
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum


class Attribute(Enum):
    """Základní vlastnosti postavy"""
    STR = "STR"  # Síla
    DEX = "DEX"  # Obratnost
    WIL = "WIL"  # Vůle


@dataclass
class Character:
    """Model pro postavu myši"""
    name: str
    background: str

    # Vlastnosti
    strength: int
    dexterity: int
    willpower: int

    # Hit Points
    max_hp: int
    current_hp: int

    # Inventář - 10 slotů
    inventory: List[Optional[str]] = field(default_factory=lambda: [None] * 10)

    # Volitelné atributy
    appearance: Optional[str] = None
    personality: Optional[str] = None
    disposition: Optional[str] = None
    birthsign: Optional[str] = None
    coat: Optional[str] = None

    # Podmínky
    conditions: List[str] = field(default_factory=list)

    # Level a XP
    level: int = 1
    experience: int = 0

    # Poznámky
    notes: str = ""


@dataclass
class Item:
    """Model pro předmět"""
    name: str
    description: str
    slots: int = 1  # Kolik slotů zabírá
    cost: Optional[int] = None  # Cena v penízích
    usage_die: Optional[str] = None  # Např. "d6" pro spotřební předměty
    tags: List[str] = field(default_factory=list)


@dataclass
class Condition:
    """Model pro kondici/stav"""
    name: str
    description: str
    effect: str
    duration: Optional[str] = None  # Např. "do konce boje", "permanentní"


@dataclass
class Background:
    """Model pro pozadí postavy"""
    name: str
    description: str
    starting_items: List[str]
    hp_bonus: int = 0


@dataclass
class Location:
    """Model pro lokaci"""
    name: str
    description: str
    rooms: List[Dict] = field(default_factory=list)
    encounters: List[str] = field(default_factory=list)
    treasures: List[str] = field(default_factory=list)


@dataclass
class NPC:
    """
    Model pro NPC (nehráčskou postavu).
    Používá se pro rychlé generování NPC podle oficiálních pravidel Mausritter.
    """
    name: str
    social_status: str  # Společenské postavení (Chuďas, Prostá myš, Měšťan, atd.)
    birthsign: str  # Rodné znamení s povahou
    appearance: str  # Vzhled
    quirk: str  # Zvláštnost
    desire: str  # Po čem touží
    relationship: str  # Vztah k jiné myši
    reaction: str  # Reakce při setkání
    payment: Optional[str] = None  # Platba za služby (podle společenského postavení)
    notes: str = ""


@dataclass
class Hireling:
    """
    Model pro pronajímatelnou myš (pomocníka).
    Používá se pro generování pomocníků podle pravidel z kapitoly Hirelings.
    """
    name: str
    type: str  # Typ pomocníka (Světlonoš, Dělník, Učenec, atd.)
    daily_wage: int  # Denní mzda v ďobcích

    # Vlastnosti
    hp: int
    strength: int
    dexterity: int
    willpower: int

    # Inventář - 6 políček (2 v packách, 2 na těle, 2 v batohu)
    inventory: List[Optional[str]] = field(default_factory=lambda: [None] * 6)

    # Level a XP
    level: int = 1
    experience: int = 0

    # Morálka a stav
    morale: str = "neutrální"  # neutrální, loajální, nespokojený
    notes: str = ""


@dataclass
class Weather:
    """
    Model pro počasí.
    Používá se pro generování denního počasí podle ročních období.
    """
    season: str  # "spring", "summer", "autumn", "winter"
    weather: str  # Popis počasí (např. "Jasno a slunečno")
    unfavorable: bool  # True pokud nepřeje cestování (vyžaduje STR save)
    event: Optional[str] = None  # Volitelná sezónní událost
    notes: str = ""
