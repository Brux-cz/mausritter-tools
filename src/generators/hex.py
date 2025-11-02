"""
HexGenerator - generátor hexů pro hexcrawl kampaně

Generuje náhodné hexy s typy a výraznými prvky podle oficiálních pravidel.
Používá Settlement Generator pro hexy s myšími osadami.

Podle oficiálních Mausritter pravidel (11_HEXCRAWL_SETUP.md).
"""

import json
from typing import Optional
from src.core.models import Hex
from src.core.tables import TableLoader
from src.core.dice import roll_d6, roll_d8
from src.generators.settlement import SettlementGenerator


class HexGenerator:
    """
    Generátor hexů pro hexcrawl kampaně podle oficiálních Mausritter pravidel.

    Mechanika:
    - Typ hexu: k6 (Otevřená krajina, Les, Řeka, Lidské město)
    - Detail: k6 (kategorie) × k8 (konkrétní detail)
    - Speciální: k6=1 generuje Settlement pomocí SettlementGenerator

    Použití:
        # Náhodný hex
        hex_obj = HexGenerator.create()

        # Hex s konkrétním typem
        hex_obj = HexGenerator.create_with_type(type_roll=3)  # Les

        # Hex s osadou
        hex_obj = HexGenerator.create_with_settlement()

        # Export do JSON
        json_str = HexGenerator.to_json(hex_obj)
    """

    @classmethod
    def create(
        cls,
        type_roll: Optional[int] = None,
        detail_category: Optional[int] = None,
        detail_subtype: Optional[int] = None
    ) -> Hex:
        """
        Vytvoř náhodný hex.

        Args:
            type_roll: Volitelný hod k6 pro typ hexu (1-6)
            detail_category: Volitelný hod k6 pro kategorii detailu (1-6)
            detail_subtype: Volitelný hod k8 pro konkrétní detail (1-8, pouze pokud category ≠ 1)

        Returns:
            Hex objekt s vygenerovanými daty
        """
        # 1. Hoď k6 pro typ hexu
        if type_roll is None:
            type_roll = roll_d6()

        # Najdi typ hexu
        hex_type_data = TableLoader.lookup_hex_type(type_roll)
        if hex_type_data is None:
            # Fallback
            hex_type = "Neznámý hex"
        else:
            hex_type = hex_type_data["name"]

        # 2. Hoď k6 pro kategorii detailu
        if detail_category is None:
            detail_category = roll_d6()

        # 3. Speciální případ: Myší osada (category=1)
        if detail_category == 1:
            # Použij Settlement Generator
            settlement = SettlementGenerator.create()

            return Hex(
                type=hex_type,
                type_roll=type_roll,
                detail_category=1,
                detail_subtype=None,
                detail_name="Myší osada",
                detail_hook="Generováno pomocí Settlement Generatoru",
                settlement=settlement,
                description=f"{settlement.name} - {settlement.size_name}"
            )

        # 4. Normální případ: Hoď k8 pro konkrétní detail
        if detail_subtype is None:
            detail_subtype = roll_d8()

        # Najdi detail
        detail_data = TableLoader.lookup_hex_detail(detail_category, detail_subtype)
        if detail_data is None:
            # Fallback
            return Hex(
                type=hex_type,
                type_roll=type_roll,
                detail_category=detail_category,
                detail_subtype=detail_subtype,
                detail_name="Neznámý detail",
                detail_hook="Popis není k dispozici",
                settlement=None,
                description=""
            )

        # 5. Vytvoř Hex objekt
        return Hex(
            type=hex_type,
            type_roll=type_roll,
            detail_category=detail_category,
            detail_subtype=detail_subtype,
            detail_name=detail_data["name"],
            detail_hook=detail_data["hook"],
            settlement=None,
            description=""
        )

    @classmethod
    def create_with_type(cls, type_roll: int) -> Hex:
        """
        Vytvoř hex s konkrétním typem.

        Args:
            type_roll: Hod k6 pro typ hexu (1-6)

        Returns:
            Hex objekt s daným typem
        """
        return cls.create(type_roll=type_roll)

    @classmethod
    def create_with_settlement(cls) -> Hex:
        """
        Vytvoř hex s myší osadou (detail_category=1).

        Returns:
            Hex objekt s osadou
        """
        return cls.create(detail_category=1)

    @staticmethod
    def to_dict(hex_obj: Hex) -> dict:
        """
        Převede Hex objekt na dictionary.

        Args:
            hex_obj: Hex objekt

        Returns:
            Dictionary s daty hexu
        """
        result = {
            "type": hex_obj.type,
            "type_roll": hex_obj.type_roll,
            "type_emoji": hex_obj.type_emoji,
            "detail": {
                "category": hex_obj.detail_category,
                "category_name": hex_obj.category_name_cz,
                "subtype": hex_obj.detail_subtype,
                "name": hex_obj.detail_name,
                "hook": hex_obj.detail_hook,
            },
            "description": hex_obj.description,
            "is_settlement": hex_obj.is_settlement,
        }

        # Pokud obsahuje settlement, přidej settlement data
        if hex_obj.is_settlement and hex_obj.settlement:
            from src.generators.settlement import SettlementGenerator
            result["settlement"] = SettlementGenerator.to_dict(hex_obj.settlement)

        return result

    @staticmethod
    def to_json(hex_obj: Hex, indent: int = 2) -> str:
        """
        Převede Hex objekt na JSON string.

        Args:
            hex_obj: Hex objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = HexGenerator.to_dict(hex_obj)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(hex_obj: Hex) -> str:
        """
        Naformátuj hex jako čitelný text.

        Args:
            hex_obj: Hex objekt

        Returns:
            Formátovaný text s informacemi o hexu
        """
        lines = []
        lines.append("═══ HEX PRO HEXCRAWL ═══")
        lines.append("")
        lines.append(f"{hex_obj.type_emoji}  {hex_obj.type}")
        lines.append(f"📋 Kategorie: {hex_obj.category_name_cz}")
        lines.append("")
        lines.append(f"🔍 Detail: {hex_obj.detail_name}")
        lines.append(f"❓ Háček: {hex_obj.detail_hook}")
        lines.append("")

        if hex_obj.is_settlement and hex_obj.settlement:
            lines.append("🏘️ MYŠÍ OSADA:")
            from src.generators.settlement import SettlementGenerator
            settlement_text = SettlementGenerator.format_text(hex_obj.settlement)
            lines.append(settlement_text)
            lines.append("")

        if hex_obj.description:
            lines.append(f"📝 Popis: {hex_obj.description}")
            lines.append("")

        hod_text = f"🎲 Hody: Typ k6={hex_obj.type_roll}, Kategorie k6={hex_obj.detail_category}"
        if hex_obj.detail_subtype:
            hod_text += f", Detail k8={hex_obj.detail_subtype}"
        lines.append(hod_text)

        return "\n".join(lines)
