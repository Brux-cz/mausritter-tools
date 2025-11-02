"""
SettlementGenerator - generátor osad

Osady jsou místa kde myši žijí, obchodují a odpočívají.
Velikost osady určuje dostupné služby a prvky.

Podle oficiálních Mausritter pravidel (12_SETTLEMENTS.md).
"""

import json
from typing import Optional, List
from src.core.models import Settlement, Tavern
from src.core.tables import TableLoader
from src.core.dice import roll_2d6_keep_lower, roll_d6, roll_d12, roll_d20
from src.generators.tavern import TavernGenerator


class SettlementGenerator:
    """
    Generátor osad podle oficiálních Mausritter pravidel.

    Mechanika:
    - Velikost: 2d6 keep-lower (1-6)
    - Vláda: k6 + sizeValue (2-12)
    - Detail: k20
    - Řemesla: 1× k20 (2× pro města A velkoměsta sizeValue 5-6)
    - Prvky: 1× k20 (2× pro velkoměsta sizeValue=6)
    - Událost: k20
    - Název: volitelný, kombinace semínek (k12 + k12)
    - Hospoda: pro velikost 3+ (Víska a větší)

    Použití:
        # Náhodná osada
        settlement = SettlementGenerator.create()

        # S konkrétními hody
        settlement = SettlementGenerator.create(
            roll_size_die1=4, roll_size_die2=2,
            roll_government=5,
            generate_name=True
        )

        # Export do JSON
        json_str = SettlementGenerator.to_json(settlement)
    """

    @classmethod
    def create(
        cls,
        roll_size_die1: Optional[int] = None,
        roll_size_die2: Optional[int] = None,
        roll_government: Optional[int] = None,
        roll_detail: Optional[int] = None,
        roll_trades: Optional[List[int]] = None,
        roll_features: Optional[List[int]] = None,
        roll_event: Optional[int] = None,
        roll_name_start: Optional[int] = None,
        roll_name_end: Optional[int] = None,
        generate_name: bool = False,
        generate_tavern: bool = True
    ) -> Settlement:
        """
        Vytvoř náhodnou osadu.

        Args:
            roll_size_die1: Volitelný první hod k6 pro velikost
            roll_size_die2: Volitelný druhý hod k6 pro velikost
            roll_government: Volitelný hod k6 pro vládu
            roll_detail: Volitelný hod k20 pro detail
            roll_trades: Volitelný list hodů k20 pro řemesla
            roll_features: Volitelný list hodů k20 pro prvky
            roll_event: Volitelný hod k20 pro událost
            roll_name_start: Volitelný hod k12 pro začátek názvu
            roll_name_end: Volitelný hod k12 pro konec názvu
            generate_name: Generovat název osady? (default: False)
            generate_tavern: Generovat hospodu pro velikost 3+? (default: True)

        Returns:
            Settlement objekt s vygenerovanými daty
        """
        # 1. Velikost osady (2d6 keep-lower)
        if roll_size_die1 is None or roll_size_die2 is None:
            size_result, die1, die2 = roll_2d6_keep_lower()
            if roll_size_die1 is None:
                roll_size_die1 = die1
            if roll_size_die2 is None:
                roll_size_die2 = die2
            if roll_size_die1 is not None and roll_size_die2 is not None:
                size_result = min(roll_size_die1, roll_size_die2)
        else:
            size_result = min(roll_size_die1, roll_size_die2)

        # Získej info o velikosti z tabulky
        size_data = TableLoader.lookup_settlement_size(size_result)
        if size_data is None:
            # Fallback
            size_name = "Neznámá osada"
            population = "?"
            size_value = size_result
            has_tavern_flag = False
            trades_count = 1
            features_count = 1
        else:
            size_name = size_data["name"]
            population = size_data["population"]
            size_value = size_data["sizeValue"]
            has_tavern_flag = size_data["hasTavern"]
            trades_count = size_data["tradesCount"]
            features_count = size_data["featuresCount"]

        # 2. Vláda (k6 + sizeValue)
        if roll_government is None:
            roll_government = roll_d6()
        government_roll = roll_government + size_value
        government = TableLoader.lookup_settlement_government(government_roll)
        if government is None:
            government = "Neznámá vláda"

        # 3. Detail (k20)
        if roll_detail is None:
            roll_detail = roll_d20()
        detail = TableLoader.lookup_settlement_detail(roll_detail)
        if detail is None:
            detail = "Běžná osada"

        # 4. Řemesla (1-2× k20 podle velikosti)
        trades = []
        trades_rolls = []
        if roll_trades is None:
            roll_trades = [roll_d20() for _ in range(trades_count)]

        for trade_roll in roll_trades[:trades_count]:
            trade = TableLoader.lookup_settlement_trade(trade_roll)
            if trade:
                trades.append(trade)
            trades_rolls.append(trade_roll)

        # 5. Prvky (1-2× k20 podle velikosti)
        features = []
        features_rolls = []
        if roll_features is None:
            roll_features = [roll_d20() for _ in range(features_count)]

        for feature_roll in roll_features[:features_count]:
            feature = TableLoader.lookup_settlement_feature(feature_roll)
            if feature:
                features.append(feature)
            features_rolls.append(feature_roll)

        # 6. Událost (k20)
        if roll_event is None:
            roll_event = roll_d20()
        event = TableLoader.lookup_settlement_event(roll_event)
        if event is None:
            event = "Nic zvláštního"

        # 7. Název (volitelný)
        name = ""
        if generate_name:
            if roll_name_start is None:
                roll_name_start = roll_d12()
            if roll_name_end is None:
                roll_name_end = roll_d12()

            # Náhodně vyber jednu z možností začátku a konce
            import random
            start_table = random.choice(["name_start_a", "name_start_b"])
            end_table = random.choice(["name_end_a", "name_end_b"])

            name_start = TableLoader.lookup_settlement_name_part(start_table, roll_name_start)
            name_end = TableLoader.lookup_settlement_name_part(end_table, roll_name_end)

            if name_start and name_end:
                # Pokud konec začíná pomlčkou, spoj ho
                if name_end.startswith("-"):
                    name = name_start + name_end
                else:
                    name = f"{name_start} {name_end}"

        # 8. Hospoda (pro velikost 3+)
        tavern = None
        if generate_tavern and has_tavern_flag:
            tavern = TavernGenerator.create()

        return Settlement(
            size_name=size_name,
            population=population,
            size_value=size_value,
            government=government,
            detail=detail,
            trades=trades,
            features=features,
            event=event,
            name=name,
            tavern=tavern,
            roll_size_die1=roll_size_die1,
            roll_size_die2=roll_size_die2,
            roll_government=roll_government,
            roll_detail=roll_detail,
            roll_trades=trades_rolls,
            roll_features=features_rolls,
            roll_event=roll_event,
            roll_name_start=roll_name_start if generate_name else 0,
            roll_name_end=roll_name_end if generate_name else 0
        )

    @staticmethod
    def to_dict(settlement: Settlement) -> dict:
        """
        Převede Settlement objekt na dictionary.

        Args:
            settlement: Settlement objekt

        Returns:
            Dictionary s daty osady
        """
        result = {
            "size": {
                "name": settlement.size_name,
                "population": settlement.population,
                "value": settlement.size_value
            },
            "government": settlement.government,
            "detail": settlement.detail,
            "trades": settlement.trades,
            "features": settlement.features,
            "event": settlement.event,
            "rolls": {
                "size_die1": settlement.roll_size_die1,
                "size_die2": settlement.roll_size_die2,
                "government": settlement.roll_government,
                "detail": settlement.roll_detail,
                "trades": settlement.roll_trades,
                "features": settlement.roll_features,
                "event": settlement.roll_event
            }
        }

        if settlement.name:
            result["name"] = settlement.name
            result["rolls"]["name_start"] = settlement.roll_name_start
            result["rolls"]["name_end"] = settlement.roll_name_end

        if settlement.tavern:
            result["tavern"] = TavernGenerator.to_dict(settlement.tavern)

        return result

    @staticmethod
    def to_json(settlement: Settlement, indent: int = 2) -> str:
        """
        Převede Settlement objekt na JSON string.

        Args:
            settlement: Settlement objekt
            indent: Počet mezer pro odsazení (default: 2)

        Returns:
            JSON string
        """
        data = SettlementGenerator.to_dict(settlement)
        return json.dumps(data, ensure_ascii=False, indent=indent)

    @staticmethod
    def format_text(settlement: Settlement) -> str:
        """
        Naformátuj osadu jako čitelný text.

        Args:
            settlement: Settlement objekt

        Returns:
            Formátovaný text s informacemi o osadě
        """
        lines = []
        lines.append("═══ OSADA ═══")
        lines.append("")

        if settlement.name:
            lines.append(f"📍 Název: {settlement.name}")

        lines.append(f"🏘️  Velikost: {settlement.size_name}")
        lines.append(f"👥 Populace: {settlement.population}")
        lines.append(f"⚖️  Vláda: {settlement.government}")
        lines.append(f"🔍 Detail: {settlement.detail}")
        lines.append("")

        if settlement.trades:
            lines.append("🛠️  Řemesla:")
            for trade in settlement.trades:
                lines.append(f"   • {trade}")
            lines.append("")

        if settlement.features:
            lines.append("🏛️  Prvky:")
            for feature in settlement.features:
                lines.append(f"   • {feature}")
            lines.append("")

        lines.append(f"📅 Událost: {settlement.event}")

        if settlement.tavern:
            lines.append("")
            lines.append("─── Hospoda ───")
            lines.append(f"🏠 {settlement.tavern.full_name}")
            lines.append(f"🍲 Specialita: {settlement.tavern.specialty}")

        lines.append("")
        size_roll_text = f"{settlement.roll_size_die1}, {settlement.roll_size_die2} → {min(settlement.roll_size_die1, settlement.roll_size_die2)}"
        lines.append(f"🎲 Hody: {size_roll_text} (velikost), {settlement.roll_government} (vláda), {settlement.roll_detail} (detail)")

        return "\n".join(lines)
