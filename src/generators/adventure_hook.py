"""
AdventureHookGenerator - generátor háčků dobrodružství

Háček poskytuje důvod, proč se myši vydají na dobrodružství.
Používá se pro motivaci hráčů na začátku kampaně nebo sezení.

Podle oficiálních Mausritter pravidel (11_HEXCRAWL_SETUP.md).
"""

import json
from typing import Optional
from src.core.models import AdventureHook
from src.core.tables import TableLoader
from src.core.dice import roll_d6


class AdventureHookGenerator:
    """
    Generátor háčků dobrodružství podle oficiálních Mausritter pravidel.

    Mechanika:
    - Háček: k6 (6 typů motivací)
    - Kategorie: personal, duty, quest, threat, treasure, survival
    - Otázky: Inspirační otázky pro GM k rozvíjení příběhu

    Použití:
        # Náhodný háček
        hook = AdventureHookGenerator.create()

        # S konkrétním hodem
        hook = AdventureHookGenerator.create(roll=1)  # Hledání ztraceného

        # Export do JSON
        json_str = AdventureHookGenerator.to_json(hook)
    """

    @classmethod
    def create(cls, roll: Optional[int] = None) -> AdventureHook:
        """
        Vytvoř náhodný háček dobrodružství.

        Args:
            roll: Volitelný hod k6 (1-6). Pokud None, hodí se náhodně.

        Returns:
            AdventureHook objekt s vygenerovanými daty
        """
        # 1. Hoď k6 pro háček
        if roll is None:
            roll = roll_d6()

        # 2. Najdi háček v tabulce
        hook_data = TableLoader.lookup_adventure_hook(roll)
        if hook_data is None:
            # Fallback
            return AdventureHook(
                hook="Neznámý háček",
                category="unknown",
                questions=[],
                roll=roll
            )

        # 3. Vytvoř AdventureHook objekt
        return AdventureHook(
            hook=hook_data["hook"],
            category=hook_data["category"],
            questions=hook_data["questions"],
            roll=roll
        )

    @staticmethod
    def to_dict(hook: AdventureHook) -> dict:
        """
        Převede AdventureHook objekt na dictionary.

        Args:
            hook: AdventureHook objekt

        Returns:
            Dictionary s daty háčku
        """
        return {
            "hook": hook.hook,
            "category": hook.category,
            "category_name": hook.category_name_cz,
            "questions": hook.questions,
            "roll": hook.roll
        }

    @staticmethod
    def to_json(hook: AdventureHook, indent: int = 2) -> str:
        """
        Převede AdventureHook objekt na JSON string.

        Args:
            hook: AdventureHook objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = AdventureHookGenerator.to_dict(hook)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(hook: AdventureHook) -> str:
        """
        Naformátuj háček jako čitelný text.

        Args:
            hook: AdventureHook objekt

        Returns:
            Formátovaný text s informacemi o háčku
        """
        lines = []
        lines.append("═══ HÁČEK DOBRODRUŽSTVÍ ═══")
        lines.append("")
        lines.append(f"{hook.category_emoji}  {hook.hook}")
        lines.append(f"📋 Kategorie: {hook.category_name_cz}")
        lines.append("")

        if hook.questions:
            lines.append("❓ Otázky pro rozvíjení:")
            for question in hook.questions:
                lines.append(f"   • {question}")
            lines.append("")

        lines.append(f"🎲 Hod: {hook.roll} (k6)")

        return "\n".join(lines)
