"""
Datové modely pro Mausritter
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


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


@dataclass
class Settlement:
    """
    Model pro osadu (settlement).

    Osady jsou místa kde myši žijí, obchodují a odpočívají.
    Velikost určuje dostupné služby a prvky.

    Generování:
    - Velikost: 2d6 keep-lower (1-6)
    - Vláda: k6 + sizeValue (2-12)
    - Detail: k20 charakteristika
    - Řemesla: 1× k20 (2× pro města sizeValue=5)
    - Prvky: 1× k20 (2× pro velkoměsta sizeValue=6)
    - Událost: k20
    - Název: kombinace semínek (volitelné)
    - Hospoda: generována pro velikost 3+ (Víska a výše)
    """
    # Size info
    size_name: str  # "Farma/zámeček", "Víska", "Město", etc.
    population: str  # "1-3 rodiny", "50-150 myší", etc.
    size_value: int  # 1-6

    # Core attributes
    government: str  # Typ vlády
    detail: str  # Charakteristický detail
    trades: List[str]  # Řemesla (1-2 podle velikosti)
    features: List[str]  # Výrazné prvky (1-2 podle velikosti)
    event: str  # Událost při příjezdu

    # Optional elements
    name: str = ""  # Název osady (volitelný)
    tavern: Optional['Tavern'] = None  # Hospoda (pro size 3+)
    is_friendly: bool = False  # Spřátelená osada (default pro středovou v hexcrawlu)
    hex_location: Optional[str] = None  # Pozice na mapě (např. "C3")

    # Rolls for reproducibility
    roll_size_die1: int = 0  # První k6 pro velikost
    roll_size_die2: int = 0  # Druhý k6 pro velikost
    roll_government: int = 0  # k6 pro vládu
    roll_detail: int = 0  # k20 pro detail
    roll_trades: List[int] = field(default_factory=list)  # 1-2× k20
    roll_features: List[int] = field(default_factory=list)  # 1-2× k20
    roll_event: int = 0  # k20 pro událost
    roll_name_start: int = 0  # k12 pro začátek názvu (volitelné)
    roll_name_end: int = 0  # k12 pro konec názvu (volitelné)

    @property
    def has_tavern(self) -> bool:
        """Má osada hospodu? (velikost 3+ = Víska a větší)"""
        return self.size_value >= 3

    @property
    def trades_count(self) -> int:
        """Počet řemesel podle velikosti"""
        return 2 if self.size_value >= 5 else 1

    @property
    def features_count(self) -> int:
        """Počet prvků podle velikosti"""
        return 2 if self.size_value >= 6 else 1


@dataclass
class AdventureHook:
    """
    Model pro háček dobrodružství.

    Háček poskytuje důvod, proč se myši vydají na dobrodružství.
    Používá se pro motivaci hráčů na začátku kampaně nebo sezení.

    Generování:
    - Háček: k6 (6 typů motivací)
    - Kategorie: personal, duty, quest, threat, treasure, survival
    - Otázky: Inspirační otázky pro rozvíjení háčku

    Příklady:
    - Hledání ztraceného člena rodiny (personal)
    - Vyšetřování na příkaz šlechtice (duty)
    - Čaroděj potřebuje přísadu (quest)
    - Tvor trápí osadu (threat)
    - Mapa k pokladu (treasure)
    - Útočiště před bouřkou (survival)
    """
    hook: str  # Text háčku
    category: str  # Kategorie (personal, duty, quest, threat, treasure, survival)
    questions: List[str]  # Inspirační otázky pro GM
    roll: int = 0  # Hod k6 (1-6)

    @property
    def category_emoji(self) -> str:
        """Vrať emoji podle kategorie háčku"""
        emoji_map = {
            "personal": "👨‍👩‍👧‍👦",  # Rodina
            "duty": "⚔️",  # Povinnost
            "quest": "🔮",  # Hledání
            "threat": "⚠️",  # Hrozba
            "treasure": "💰",  # Poklad
            "survival": "🌪️",  # Přežití
        }
        return emoji_map.get(self.category, "🎯")

    @property
    def category_name_cz(self) -> str:
        """Vrať český název kategorie"""
        names = {
            "personal": "Osobní",
            "duty": "Povinnost",
            "quest": "Úkol",
            "threat": "Hrozba",
            "treasure": "Poklad",
            "survival": "Přežití",
        }
        return names.get(self.category, "Jiné")


@dataclass
class CreatureVariant:
    """Varianta stvoření (Ghost Ability, Snake Type, atd.)"""

    name: str
    description: str
    creature_type: str
    roll: int = 0

    @property
    def creature_emoji(self) -> str:
        """Vrať emoji pro typ stvoření"""
        emoji_map = {
            "ghost": "👻",
            "snake": "🐍",
            "cat": "🐱",
            "rat": "🐀",
            "mouse": "🐭",
            "spider": "🕷️",
            "owl": "🦉",
            "centipede": "🐛",
            "fairy": "🧚",
            "crow": "🦅",
            "frog": "🐸",
        }
        return emoji_map.get(self.creature_type, "🦎")

    @property
    def creature_name_cz(self) -> str:
        """Vrať český název typu stvoření"""
        names = {
            "ghost": "Přízrak",
            "snake": "Had",
            "cat": "Kočka",
            "rat": "Krysa",
            "mouse": "Myš",
            "spider": "Pavouk",
            "owl": "Sova",
            "centipede": "Stonožka",
            "fairy": "Víla",
            "crow": "Vrána",
            "frog": "Žába",
        }
        return names.get(self.creature_type, "Stvoření")

    @property
    def variant_table_name_cz(self) -> str:
        """Vrať český název tabulky variant"""
        names = {
            "ghost": "Přízračné schopnosti",
            "snake": "Zvláštní hadi",
            "cat": "Kočičí pánové a paní",
            "rat": "Krysí gangy",
            "mouse": "Konkurenční myší dobrodruzi",
            "spider": "Druhy pavouků",
            "owl": "Soví čarodějové",
            "centipede": "Zevlující stonožky",
            "fairy": "Vílí plány",
            "crow": "Vraní písně",
            "frog": "Potulní žabí rytíři",
        }
        return names.get(self.creature_type, "Varianty stvoření")


@dataclass
class Hex:
    """Hex pro hexcrawl kampaň"""

    type: str
    type_roll: int
    detail_category: int
    detail_subtype: Optional[int]
    detail_name: str
    detail_hook: str
    settlement: Optional['Settlement'] = None
    description: str = ""

    @property
    def type_emoji(self) -> str:
        """Vrať emoji pro typ hexu"""
        emoji_map = {
            "Otevřená krajina": "🌾",
            "Les": "🌲",
            "Řeka": "🌊",
            "Lidské město": "🏛️",
        }
        return emoji_map.get(self.type, "🗺️")

    @property
    def is_settlement(self) -> bool:
        """True pokud hex obsahuje myší osadu"""
        return self.detail_category == 1 and self.settlement is not None

    @property
    def category_name_cz(self) -> str:
        """Vrať český název kategorie detailu"""
        names = {
            1: "Myší osada",
            2: "Civilizační prvky",
            3: "Zvířecí a přírodní prvky",
            4: "Přírodní a opuštěné prvky",
            5: "Mystické prvky",
            6: "Pradávné a lidské prvky",
        }
        return names.get(self.detail_category, "Neznámá kategorie")


@dataclass
class Room:
    """Místnost v dobrodružném místě (dungeonu)"""

    room_number: int
    room_type: str
    room_type_roll: int
    has_creature: bool
    has_treasure: bool
    feature: Optional[str] = None
    feature_roll: Optional[int] = None

    @property
    def type_emoji(self) -> str:
        """Vrať emoji pro typ místnosti"""
        emoji_map = {
            "Prázdná": "⬜",
            "Překážka": "🚧",
            "Past": "⚠️",
            "Hlavolam": "🧩",
            "Doupě": "🏰",
        }
        return emoji_map.get(self.room_type, "❓")


@dataclass
class Dungeon:
    """Dobrodružné místo (dungeon) pro kampaň"""

    past: str
    past_roll: int
    decay: str
    decay_roll: int
    inhabitants: str
    inhabitants_roll: int
    goal: str
    goal_roll: int
    secret: str
    secret_roll: int
    rooms: List['Room']
    settlement: Optional['Settlement'] = None
    description: str = ""

    @property
    def has_settlement(self) -> bool:
        """True pokud dungeon obsahuje myší osadu"""
        return self.past_roll == 20 and self.settlement is not None

    @property
    def room_count(self) -> int:
        """Počet místností v dungeonu"""
        return len(self.rooms)


@dataclass
class Rumor:
    """
    Model pro zvěst/fámu v hexcrawl kampani.

    Kombinuje 4 přístupy:
    - B (World-Connected): Zvěsti o reálných místech z hexcrawlu
    - D (Categories): Organizace do kategorií
    - C (Story Hooks): k6×k6 tabulky pro komplexní zápletky
    - E (Gossip Network): Simulace šíření a zkreslení přes NPC

    Pravdivost (podle k6 hodu):
    - 1-3: true (50% šance) - pravdivá zvěst
    - 4-5: partial (33% šance) - částečně pravdivá
    - 6: false (17% šance) - fáma
    """

    roll: int  # Hod k6 (1-6)
    rumor_text: str  # Finální text zvěsti
    category: str  # Kategorie: "threat", "npc", "location", "treasure", "mystery"
    truthfulness: str  # "true", "partial", "false"

    # World-Connected data (Variant B)
    source_location: Optional[Dict] = None  # Data o zdrojové lokaci (settlement/hex/dungeon)

    # Gossip Network data (Variant E)
    gossip_hops: int = 0  # Počet "telefonních hopů" (0-3)
    gossip_chain: List[str] = field(default_factory=list)  # Řetězec: [pravda, hop1, hop2, ...]

    # Story Hook data (Variant C)
    story_hook_detail: Optional[str] = None  # Detail z k6×k6 tabulky

    # GM notes
    truth_part: Optional[str] = None  # Co je pravda (pro partial/false)
    false_part: Optional[str] = None  # Co je lež (pro partial/false)
    gm_notes: str = ""  # Poznámky pro GM

    @property
    def category_emoji(self) -> str:
        """Vrať emoji podle kategorie zvěsti"""
        emoji_map = {
            "threat": "🗡️",
            "npc": "👤",
            "location": "📍",
            "treasure": "💎",
            "mystery": "🔮",
        }
        return emoji_map.get(self.category, "❓")

    @property
    def truthfulness_symbol(self) -> str:
        """Vrať symbol pravdivosti"""
        symbols = {
            "true": "✓",
            "partial": "~",
            "false": "✗",
        }
        return symbols.get(self.truthfulness, "?")

    @property
    def truthfulness_name_cz(self) -> str:
        """Vrať český název pravdivosti"""
        names = {
            "true": "PRAVDA",
            "partial": "ČÁSTEČNĚ",
            "false": "FÁMA",
        }
        return names.get(self.truthfulness, "NEZNÁMÉ")

    @property
    def category_name_cz(self) -> str:
        """Vrať český název kategorie"""
        names = {
            "threat": "Hrozba",
            "npc": "NPC",
            "location": "Lokace",
            "treasure": "Poklad",
            "mystery": "Tajemství",
        }
        return names.get(self.category, "Jiné")


@dataclass
class Hexcrawl:
    """
    Kompletní hexcrawl podle oficiálních pravidel Mausritter.

    VŽDY obsahuje 5×5 mapu (25 hexů) jak doporučuje rulebook (str. 21).

    Komponenty:
    - 25 hexů (jednomílových)
    - 1-3 settlements (osady)
    - 2-4 dungeons (adventure sites)
    - 6 rumors (k6 tabulka zvěstí)
    - 0-4 frakce (volitelné, zatím neimplementováno)

    Zdroj: docs/knowledge_base/11_HEXCRAWL_SETUP.md
    """
    hexes: List['Hex']
    settlements: List[Settlement]
    dungeons: List['Dungeon']
    rumors: List[Rumor]
    world_state: Dict[str, Any]
    factions: List[Any] = field(default_factory=list)  # Placeholder pro FactionGenerator
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validace a inicializace metadata při vytvoření."""
        # KRITICKÁ VALIDACE: Hexcrawl MUSÍ mít přesně 25 hexů!
        if len(self.hexes) != 25:
            raise ValueError(
                f"Hexcrawl musí mít přesně 25 hexů (5×5 podle oficiálních pravidel), "
                f"ale má {len(self.hexes)}. "
                f"Zdroj: Mausritter Rulebook str. 21"
            )

        # Inicializuj metadata
        self.metadata = {
            "generated_at": datetime.now().isoformat(),
            "generator_version": "1.0.0",
            "map_dimensions": "5x5",
            "official_rules_compliant": True,
            "counts": {
                "hexes": 25,
                "settlements": len(self.settlements),
                "dungeons": len(self.dungeons),
                "rumors": len(self.rumors),
                "factions": len(self.factions)
            }
        }

    @property
    def map_dimensions(self) -> tuple:
        """Vrať rozměry mapy (vždy 5×5 podle oficiálních pravidel)."""
        return (5, 5)

    def to_dict(self) -> Dict[str, Any]:
        """Konvertuj na dictionary pro export."""
        return {
            "metadata": self.metadata,
            "world_state": self.world_state,
            "hexes": [asdict(h) for h in self.hexes],
            "settlements": [asdict(s) for s in self.settlements],
            "dungeons": [asdict(d) for d in self.dungeons],
            "rumors": [asdict(r) for r in self.rumors],
            "factions": self.factions  # Prázdné pro teď
        }
