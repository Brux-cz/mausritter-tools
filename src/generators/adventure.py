"""
Generátor semínek dobrodružství podle oficiálních pravidel Mausritter.

Zdroj: Mausritter CZ - pravidla.pdf, str. 16_RANDOM_TABLES.md (Adventure Seeds)

Mechanika:
- k66 (první d6 = desítky, druhá d6 = jednotky)
- 36 možných kombinací (11-66)
- Dvě možnosti: jeden hod → celý řádek, nebo tři hody → custom kombinace
"""

from typing import Optional, Dict, Any
from dataclasses import asdict
import json

from src.core.dice import roll_d66
from src.core.models import AdventureSeed
from src.core.tables import TableLoader


class AdventureSeedGenerator:
    """
    Generátor náhodných semínek dobrodružství podle pravidel Mausritter.

    Semínko dobrodružství kombinuje:
    - **Tvora** (KDO je zapojen)
    - **Problém** (CO se stalo)
    - **Komplikaci** (JAK je to složité)

    Použití:
        >>> # Základní generování (jeden hod k66)
        >>> seed = AdventureSeedGenerator.create()
        >>> print(f"{seed.creature}: {seed.problem} - {seed.complication}")
        >>>
        >>> # Custom kombinace (tři hody k66)
        >>> seed = AdventureSeedGenerator.create_custom()
    """

    @classmethod
    def create(cls, roll: Optional[int] = None) -> AdventureSeed:
        """
        Vytvoř náhodné semínko dobrodružství.

        Podle pravidel: "Hoď jednou a přečti celý řádek"

        Args:
            roll: Volitelný k66 hod (11-66), jinak náhodný

        Returns:
            AdventureSeed instance

        Example:
            >>> seed = AdventureSeedGenerator.create()
            >>> assert seed.creature
            >>> assert seed.problem
            >>> assert seed.complication
            >>> assert 11 <= seed.roll <= 66
        """
        # Hoď k66 pokud není zadáno
        if roll is None:
            roll = roll_d66()

        # Lookup v tabulce
        seed_data = TableLoader.lookup_adventure_seed(roll)

        if not seed_data:
            # Fallback - nemělo by nastat pokud jsou data správná
            return AdventureSeed(
                roll=roll,
                creature="Neznámý tvor",
                problem="Má problém",
                complication="Je to komplikované",
                notes="Chyba: Nenalezeno v tabulce"
            )

        # Vytvoř AdventureSeed objekt
        seed = AdventureSeed(
            roll=seed_data["roll"],
            creature=seed_data["creature"],
            problem=seed_data["problem"],
            complication=seed_data["complication"],
            notes=""
        )

        return seed

    @classmethod
    def create_custom(cls,
                     creature_roll: Optional[int] = None,
                     problem_roll: Optional[int] = None,
                     complication_roll: Optional[int] = None) -> AdventureSeed:
        """
        Vytvoř custom semínko dobrodružství s oddělnými hody.

        Podle pravidel: "hoď na každý sloupec zvlášť"

        Umožňuje kombinovat různé tvory, problémy a komplikace
        pro vytvoření unikátního semínka.

        Args:
            creature_roll: k66 hod pro tvora (11-66)
            problem_roll: k66 hod pro problém (11-66)
            complication_roll: k66 hod pro komplikaci (11-66)

        Returns:
            AdventureSeed instance s kombinací (roll=0 pro custom)

        Example:
            >>> # Kompletně náhodná custom kombinace
            >>> seed = AdventureSeedGenerator.create_custom()
            >>>
            >>> # Specifická kombinace
            >>> seed = AdventureSeedGenerator.create_custom(
            ...     creature_roll=11,  # Rybář
            ...     problem_roll=22,   # Zničený domov
            ...     complication_roll=33  # Sledují ho pomocí čipu
            ... )
        """
        # Hoď k66 pro každou složku pokud není zadáno
        if creature_roll is None:
            creature_roll = roll_d66()
        if problem_roll is None:
            problem_roll = roll_d66()
        if complication_roll is None:
            complication_roll = roll_d66()

        # Lookup pro každou složku
        creature_data = TableLoader.lookup_adventure_seed(creature_roll)
        problem_data = TableLoader.lookup_adventure_seed(problem_roll)
        complication_data = TableLoader.lookup_adventure_seed(complication_roll)

        # Vytvoř kombinované semínko
        seed = AdventureSeed(
            roll=0,  # Custom kombinace nemá jediný roll
            creature=creature_data["creature"] if creature_data else "Neznámý tvor",
            problem=problem_data["problem"] if problem_data else "Má problém",
            complication=complication_data["complication"] if complication_data else "Je složité",
            notes=f"Custom kombinace: {creature_roll}/{problem_roll}/{complication_roll}"
        )

        return seed

    @staticmethod
    def to_dict(seed: AdventureSeed) -> Dict[str, Any]:
        """
        Konvertuj AdventureSeed do dictionary.

        Args:
            seed: AdventureSeed instance

        Returns:
            Dictionary reprezentace

        Example:
            >>> seed = AdventureSeedGenerator.create()
            >>> data = AdventureSeedGenerator.to_dict(seed)
            >>> assert "creature" in data
        """
        return asdict(seed)

    @staticmethod
    def to_json(seed: AdventureSeed, indent: int = 2) -> str:
        """
        Konvertuj AdventureSeed do JSON stringu.

        Args:
            seed: AdventureSeed instance
            indent: Odsazení pro formátování

        Returns:
            JSON string s českými znaky

        Example:
            >>> seed = AdventureSeedGenerator.create()
            >>> json_str = AdventureSeedGenerator.to_json(seed)
            >>> assert "creature" in json_str
        """
        data = AdventureSeedGenerator.to_dict(seed)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(seed: AdventureSeed) -> str:
        """
        Formátuj semínko jako čitelný víceřádkový text.

        Args:
            seed: AdventureSeed instance

        Returns:
            Formátovaný string s popisem dobrodružství

        Example:
            >>> seed = AdventureSeedGenerator.create()
            >>> text = AdventureSeedGenerator.format_text(seed)
            >>> print(text)
            ═══ SEMÍNKO DOBRODRUŽSTVÍ ═══

            Tvor: Rybář
            Problém: Obviněn ze zločinu
            Komplikace: Může za to pomocník hráčské myši
        """
        lines = []

        lines.append("═══ SEMÍNKO DOBRODRUŽSTVÍ ═══")
        lines.append("")
        lines.append(f"🎭 Tvor: {seed.creature}")
        lines.append(f"⚠️  Problém: {seed.problem}")
        lines.append(f"💥 Komplikace: {seed.complication}")
        lines.append("")

        if seed.roll > 0:
            lines.append(f"📜 (Hod k66: {seed.roll})")
        else:
            lines.append("📜 (Custom kombinace)")

        if seed.notes:
            lines.append("")
            lines.append(f"📝 Poznámky: {seed.notes}")

        return "\n".join(lines)

    @staticmethod
    def get_inspiration_text(seed: AdventureSeed) -> str:
        """
        Vygeneruj inspirační text pro GM.

        Args:
            seed: AdventureSeed instance

        Returns:
            Text s otázkami a nápady pro rozvíjení dobrodružství

        Example:
            >>> seed = AdventureSeedGenerator.create()
            >>> text = AdventureSeedGenerator.get_inspiration_text(seed)
        """
        lines = []

        lines.append("💡 INSPIRACE PRO GM:")
        lines.append("")
        lines.append(f"KDO: {seed.creature}")
        lines.append(f"  → Jaké má motivace? Jak vypadá?")
        lines.append("")
        lines.append(f"CO: {seed.problem}")
        lines.append(f"  → Jak se to stalo? Kde to je?")
        lines.append("")
        lines.append(f"JAK: {seed.complication}")
        lines.append(f"  → Proč je to složité? Co může selhat?")
        lines.append("")
        lines.append("❓ OTÁZKY K ROZVÍJENÍ:")
        lines.append("  - Kde se hráčské myši s tímto setkají?")
        lines.append("  - Proč by jim mělo záležet?")
        lines.append("  - Jaká je odměna za pomoc?")
        lines.append("  - Co se stane, když to ignorují?")

        return "\n".join(lines)
