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


@dataclass
class Reaction:
    """
    Model pro reakci NPC/tvora při setkání.
    Používá se pro určení počáteční dispozice tvora k hráčským postavám.
    """
    roll: int  # Výsledek hodu 2k6 (2-12)
    reaction: str  # Typ reakce (Agresivní, Nepřátelská, Nejistá, Povídavá, Nápomocná)
    question: str  # GM otázka pro inspiraci
    notes: str = ""


@dataclass
class Spell:
    """
    Model pro kouzlo.
    Používá se pro generování náhodných kouzel při objevování pokladů.

    Note: [POČET] a [SOUČET] jsou placeholdery pro casting, ne pro generation.
    Při sesílání: [POČET] = počet kostek, [SOUČET] = součet hodnot.
    """
    roll: int  # Výsledek hodu 2d8 (2-16)
    name: str  # Název kouzla
    effect: str  # Popis efektu (s placeholdery [POČET] a [SOUČET])
    recharge: str  # Podmínka dobití kouzla
    tags: List[str] = field(default_factory=list)  # Kategorie (damage, healing, utility, atd.)
    notes: str = ""


@dataclass
class Tool:
    """
    Model pro nástroj.
    Používá se v pokladech a jako běžné vybavení.
    """
    name: str  # Název nástroje
    value: int  # Cena v ďobcích
    slots: int = 1  # Počet políček v inventáři (default 1)
    usage_dots: int = 0  # Počet teček použití (0 = bez teček)
    origin: str = "myší"  # "myší" nebo "lidská" výroba
    notes: str = ""


@dataclass
class Armor:
    """
    Model pro zbroj.
    Používá se v pokladech a jako běžné vybavení.
    """
    type: str  # Typ zbroje (Lehká zbroj, Těžká zbroj, Štít)
    examples: str  # Příklady (kabátec, kožený límec, atd.)
    protection: str  # Popis ochrany
    slots: str  # Popis políček (slovní)
    slots_count: int  # Počet políček (číselně)
    value: int  # Cena v ďobcích
    notes: str = ""


@dataclass
class MagicSword:
    """
    Model pro kouzelný meč.
    Používá se při generování pokladů (1/20 šance na hlavní tabulce).

    Tečky použití se zaškrtávají JENOM když padne 6 při útoku.
    Oprava: pouze velmi šikovný kovář nebo praktický čaroděj (za víc než ďobky).
    """
    weapon_type: str  # Typ zbraně: "Střední", "Lehká", "Těžká"
    damage: str  # Zranění: "k6/k8", "k6", "k10"
    name: str  # Název meče (Tepané železo, Hadí zub, atd.)
    ability: str  # Popis schopnosti
    trigger: str  # Kdy se aktivuje: "passive", "critical"
    effect_type: str  # Typ efektu: "defensive", "damage", "utility", "buff", "debuff"
    tags: List[str] = field(default_factory=list)  # Tagy pro kategorizaci
    usage_dots: int = 3  # Tečky použití (default 3)
    cursed: bool = False  # Je prokletý?
    curse: Optional[str] = None  # Popis kletby (pokud cursed=True)
    curse_lift: Optional[str] = None  # Podmínka sejmutí kletby
    notes: str = ""


@dataclass
class TreasureItem:
    """
    Model pro obecnou položku pokladu.
    Může reprezentovat ďobky, předmět z tabulky, kouzlo, nebo kouzelný meč.
    """
    type: str  # Typ: "pips", "trinket", "valuable", "bulky", "unusual", "useful", "spell", "magic_sword"
    name: str  # Název položky
    description: Optional[str] = None  # Detailní popis
    value: Optional[int] = None  # Hodnota v ďobcích (může být None pro speciální předměty)
    slots: int = 1  # Počet políček v inventáři
    usage_dots: int = 0  # Počet teček použití

    # Pro speciální typy
    spell: Optional[Spell] = None  # Pokud type="spell"
    magic_sword: Optional[MagicSword] = None  # Pokud type="magic_sword"
    tool: Optional[Tool] = None  # Pokud type="tool" (v užitečném pokladu)
    armor: Optional[Armor] = None  # Pokud type="armor" (v užitečném pokladu)

    # Metadata
    buyer: Optional[str] = None  # Kdo to koupí (pro neobvyklý poklad)
    quantity: int = 1  # Počet kusů (např. k6 zásob)
    notes: str = ""


@dataclass
class TreasureHoard:
    """
    Model pro celý poklad (hoard).
    Obsahuje seznam položek vygenerovaných z hlavní tabulky.

    Počet položek závisí na bonusových otázkách:
    - 2 základní hody k20
    - +0 až +4 bonusové hody (za kladné odpovědi na otázky)
    - Celkem 2-6 položek
    """
    items: List[TreasureItem] = field(default_factory=list)  # Seznam položek pokladu
    total_value: int = 0  # Celková hodnota v ďobcích (bez neprodejných předmětů)
    bonus_rolls: int = 0  # Počet bonusových hodů (0-4)
    total_rolls: int = 2  # Celkový počet hodů k20 (2-6)
    notes: str = ""


@dataclass
class AdventureSeed:
    """
    Model pro semínko dobrodružství.

    Kombinuje Tvora, Problém a Komplikaci podle oficiálních pravidel Mausritter.
    Používá se pro inspiraci při tvorbě dobrodružství.

    Dvě možnosti generování:
    - Jeden hod k66 → celý řádek (Tvor + Problém + Komplikace)
    - Tři hody k66 → custom kombinace sloupců
    """
    roll: int  # k66 hod (11-66), nebo 0 pro custom kombinaci
    creature: str  # Tvor zapojen do situace (KDO)
    problem: str  # Co se stalo (CO)
    complication: str  # Co to zhoršuje (JAK)
    notes: str = ""  # Volitelné poznámky GM


@dataclass
class Tavern:
    """
    Model pro hospodu/hostinec.

    Hospody se objevují ve vískách a větších osadách.
    Poskytují jídlo, pití a přístřeší pro místní i pocestné.

    Generování:
    - Název: 2× k12 (přídavné jméno + podstatné jméno)
    - Formát: "U [Část1] [Část2]" (např. "U Bílého Brouka")
    - Specialita: 1× k12 (pokrm nebo nápoj)
    """
    name_part1: str  # Přídavné jméno (k12)
    name_part2: str  # Podstatné jméno (k12)
    specialty: str  # Specialita hostince (k12)
    roll_part1: int = 0  # Hod k12 pro část 1
    roll_part2: int = 0  # Hod k12 pro část 2
    roll_specialty: int = 0  # Hod k12 pro specialitu

    @property
    def full_name(self) -> str:
        """Vrať plný název hospody ve formátu 'U [Část1] [Část2]'"""
        # Skloňování podle gramatiky (genitiv)
        part1_genitive = self._to_genitive(self.name_part1)
        part2_genitive = self._to_genitive(self.name_part2)
        return f"U {part1_genitive} {part2_genitive}"

    def _to_genitive(self, word: str) -> str:
        """Převeď slovo do genitivu (2. pádu)"""
        # Jednoduchá pravidla pro genitiv
        if word.endswith("ý"):
            return word[:-1] + "ého"
        elif word.endswith("í"):
            return word[:-1] + "ího"
        elif word in ["Brouk", "Špalek", "Sýr", "Orel", "Červ", "Rytíř"]:
            return word + "a"
        elif word in ["Liška", "Krysa", "Včela", "Lucerna", "Růže"]:
            return word[:-1] + "y"
        elif word == "Semínko":
            return "Semínka"
        else:
            return word
