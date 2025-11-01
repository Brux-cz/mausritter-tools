"""
Generátor pokladů podle oficiálních pravidel Mausritter.

Zdroj: Mausritter CZ - pravidla.pdf, str. 38-39 (Krysarií poklad / Hoard)

Mechanika:
- 2× k20 základní hody na hlavní tabulku
- +0 až +4 bonusové hody k20 (za kladné odpovědi na bonusové otázky)
- Celkem 2-6 hodů k20
- Každý hod může vést k dalším hodům na podtabulky (k6, k10, 2d8)
"""

import random
from typing import List, Optional
from src.core.models import (
    TreasureHoard, TreasureItem, MagicSword, Spell, Tool, Armor
)
from src.core.tables import TableLoader
from src.core.dice import roll_d6, roll_d8, roll_d20
from src.generators.spell import SpellGenerator


class TreasureGenerator:
    """
    Generátor pokladů (Hoard) podle oficiálních pravidel Mausritter.

    Použití:
        >>> hoard = TreasureGenerator.create(bonus_rolls=2)
        >>> print(f"Celkem {len(hoard.items)} položek")
        >>> print(f"Hodnota: {hoard.total_value} ď")
    """

    @staticmethod
    def create(bonus_rolls: int = 0) -> TreasureHoard:
        """
        Vygeneruj poklad s bonusovými hody.

        Args:
            bonus_rolls: Počet bonusových hodů k20 (0-4)
                        Každá kladná odpověď na bonusovou otázku = +1 hod

        Returns:
            TreasureHoard s 2-6 položkami

        Example:
            >>> # Poklad v běžné lokaci (0 bonusů)
            >>> hoard = TreasureGenerator.create(0)
            >>>
            >>> # Poklad v bývalé myší osadě střežený medvědem (3 bonusy)
            >>> hoard = TreasureGenerator.create(3)
        """
        if bonus_rolls < 0 or bonus_rolls > 4:
            raise ValueError("bonus_rolls musí být 0-4")

        total_rolls = 2 + bonus_rolls
        items = []

        # Proveď všechny hody na hlavní tabulku
        for _ in range(total_rolls):
            roll = roll_d20()
            item = TreasureGenerator._resolve_main_table(roll)
            if item:
                items.append(item)

        # Spočítej celkovou hodnotu (pouze prodejné předměty)
        total_value = sum(
            item.value for item in items
            if item.value is not None
        )

        return TreasureHoard(
            items=items,
            total_value=total_value,
            bonus_rolls=bonus_rolls,
            total_rolls=total_rolls
        )

    @staticmethod
    def _resolve_main_table(roll: int) -> Optional[TreasureItem]:
        """
        Vyhodnoť hod na hlavní tabulce pokladu.

        Args:
            roll: Výsledek hodu k20 (1-20)

        Returns:
            TreasureItem nebo None
        """
        entry = TableLoader.lookup_treasure_main(roll)
        if not entry:
            return None

        entry_type = entry.get("type")

        # 1. Kouzelný meč (k20 = 1)
        if entry_type == "magic_sword":
            return TreasureGenerator._generate_magic_sword_item()

        # 2. Náhodné kouzlo (k20 = 2)
        elif entry_type == "spell":
            return TreasureGenerator._generate_spell_item()

        # 3. Drobnost (k20 = 3)
        elif entry_type == "trinket":
            roll_k6 = roll_d6()
            trinket_data = TableLoader.lookup_trinket(roll_k6)
            if trinket_data:
                return TreasureItem(
                    type="trinket",
                    name=trinket_data["name"],
                    description=trinket_data["description"],
                    value=trinket_data.get("value"),
                    slots=trinket_data.get("slots", 1),
                    usage_dots=trinket_data.get("usage_dots", 0),
                    notes=trinket_data.get("notes", "")
                )

        # 4. Cenný poklad (k20 = 4)
        elif entry_type == "valuable":
            roll_k6 = roll_d6()
            valuable_data = TableLoader.lookup_valuable(roll_k6)
            if valuable_data:
                return TreasureItem(
                    type="valuable",
                    name=valuable_data["name"],
                    description=valuable_data["description"],
                    value=valuable_data.get("value"),
                    slots=valuable_data.get("slots", 1),
                    usage_dots=valuable_data.get("usage_dots", 0),
                    notes=valuable_data.get("notes", "")
                )

        # 5. Neobvyklý poklad (k20 = 5)
        elif entry_type == "unusual":
            roll_k6 = roll_d6()
            unusual_data = TableLoader.lookup_unusual(roll_k6)
            if unusual_data:
                return TreasureItem(
                    type="unusual",
                    name=unusual_data["name"],
                    description=unusual_data["description"],
                    value=unusual_data.get("value"),
                    slots=unusual_data.get("slots", 1),
                    usage_dots=unusual_data.get("usage_dots", 0),
                    buyer=unusual_data.get("buyer"),
                    notes=unusual_data.get("notes", "")
                )

        # 6-8. Objemný poklad (k20 = 6-8)
        elif entry_type == "bulky":
            roll_k6 = roll_d6()
            bulky_data = TableLoader.lookup_bulky(roll_k6)
            if bulky_data:
                return TreasureItem(
                    type="bulky",
                    name=bulky_data["name"],
                    description=bulky_data["description"],
                    value=bulky_data.get("value"),
                    slots=bulky_data.get("slots", 1),
                    usage_dots=bulky_data.get("usage_dots", 0),
                    notes=bulky_data.get("notes", "")
                )

        # 9-10. Užitečný poklad (k20 = 9-10)
        elif entry_type == "useful":
            roll_k6 = roll_d6()
            useful_data = TableLoader.lookup_useful(roll_k6)
            if useful_data:
                return TreasureGenerator._resolve_useful_item(useful_data, roll_k6)

        # 11. Bedna s k6 × 100 ďobků (k20 = 11)
        elif entry_type == "pips" and roll == 11:
            pips = roll_d6() * 100
            return TreasureItem(
                type="pips",
                name=f"Bedna s {pips} ďobků",
                description="Bedna naplněná ďobky",
                value=pips,
                slots=2,
                notes="Objemná bedna s penězmi"
            )

        # 12-14. Pytel s k6 × 50 ďobků (k20 = 12-14)
        elif entry_type == "pips" and roll in [12, 13, 14]:
            pips = roll_d6() * 50
            return TreasureItem(
                type="pips",
                name=f"Pytel s {pips} ďobků",
                description="Pytel naplněný ďobky",
                value=pips,
                slots=1,
                notes="Pytel s penězmi"
            )

        # 15-17. Peněženka s k6 × 10 ďobků (k20 = 15-17)
        elif entry_type == "pips" and roll in [15, 16, 17]:
            pips = roll_d6() * 10
            return TreasureItem(
                type="pips",
                name=f"Peněženka s {pips} ďobků",
                description="Malá peněženka s ďobky",
                value=pips,
                slots=1,
                notes="Malá peněženka"
            )

        # 18-20. Volně rozsypaných k6 × 5 ďobků (k20 = 18-20)
        elif entry_type == "pips" and roll in [18, 19, 20]:
            pips = roll_d6() * 5
            return TreasureItem(
                type="pips",
                name=f"Volně rozsypaných {pips} ďobků",
                description="Rozsypané ďobky na zemi",
                value=pips,
                slots=0,
                notes="Volně ležící peníze"
            )

        return None

    @staticmethod
    def _resolve_useful_item(useful_data: dict, roll: int) -> Optional[TreasureItem]:
        """
        Vyhodnoť užitečný poklad (může vyžadovat další generování).

        Args:
            useful_data: Data z tabulky užitečného pokladu
            roll: Hod k6 (1-6)

        Returns:
            TreasureItem
        """
        item_type = useful_data.get("type")

        # 1. k6 balení zásob
        if item_type == "supplies":
            quantity = roll_d6()
            return TreasureItem(
                type="supplies",
                name=f"{quantity}× Zásoby",
                description="Dobře zachovalé cestovní zásoby",
                value=quantity * 5,  # 5 ď za balení
                slots=quantity,
                usage_dots=3,  # Každé balení má ○○○
                quantity=quantity,
                notes=f"{quantity} balení zásob (○○○)"
            )

        # 2. k6 svazků pochodní
        elif item_type == "torches":
            quantity = roll_d6()
            return TreasureItem(
                type="torches",
                name=f"{quantity}× Pochodně",
                description="Svazky pochodní v dobrém stavu",
                value=quantity * 10,  # 10 ď za svazek
                slots=quantity,
                usage_dots=3,  # Každý svazek má ○○○
                quantity=quantity,
                notes=f"{quantity} svazky pochodní (○○○, každá tečka = 6 směn)"
            )

        # 3. Běžná zbraň
        elif item_type == "weapon":
            weapon_data = TableLoader.get_random_weapon()
            if weapon_data:
                return TreasureItem(
                    type="weapon",
                    name=weapon_data["name"],
                    description=f"Zbraň: {weapon_data['name']}",
                    value=weapon_data.get("cost", 20),
                    slots=1,
                    notes=f"Zranění: {weapon_data.get('damage', 'k6')}"
                )

        # 4. Běžná zbroj
        elif item_type == "armor":
            armor_data = TableLoader.get_random_armor()
            if armor_data:
                armor_obj = Armor(
                    type=armor_data["type"],
                    examples=armor_data["examples"],
                    protection=armor_data["protection"],
                    slots=armor_data["slots"],
                    slots_count=armor_data["slots_count"],
                    value=armor_data["value"],
                    notes=armor_data.get("notes", "")
                )
                return TreasureItem(
                    type="armor",
                    name=armor_data["type"],
                    description=f"{armor_data['examples']}",
                    value=armor_data["value"],
                    slots=armor_data["slots_count"],
                    armor=armor_obj,
                    notes=armor_data["protection"]
                )

        # 5. Běžný nástroj
        elif item_type == "tool":
            tool_data = TableLoader.get_random_tool()
            if tool_data:
                tool_obj = Tool(
                    name=tool_data["name"],
                    value=tool_data["value"],
                    slots=tool_data.get("slots", 1),
                    usage_dots=tool_data.get("usage_dots", 0),
                    origin=tool_data.get("origin", "myší"),
                    notes=tool_data.get("notes", "")
                )
                return TreasureItem(
                    type="tool",
                    name=tool_data["name"],
                    description=f"Nástroj ({tool_data.get('origin', 'myší')} výroba)",
                    value=tool_data["value"],
                    slots=tool_data.get("slots", 1),
                    usage_dots=tool_data.get("usage_dots", 0),
                    tool=tool_obj,
                    notes=tool_data.get("notes", "")
                )

        # 6. Ztracená myš ochotná pomoct (NPC/pomocník)
        elif item_type == "hireling":
            return TreasureItem(
                type="hireling",
                name="Ztracená myš ochotná pomoct",
                description="NPC myš připravená připojit se k družině",
                value=None,  # Neprodejné
                slots=0,
                notes="Generuj NPC nebo pomocníka pomocí NPC/Hireling generátoru"
            )

        return None

    @staticmethod
    def _generate_magic_sword_item() -> TreasureItem:
        """
        Vygeneruj kouzelný meč jako TreasureItem.

        Kroky:
        1. Hoď k6 na typ zbraně (Střední/Lehká/Těžká)
        2. Hoď k10 na schopnost meče
        3. Hoď k6 pro prokletí (1/6 šance)

        Returns:
            TreasureItem s MagicSword objektem
        """
        # 1. Typ zbraně (k6)
        type_roll = roll_d6()
        type_data = TableLoader.lookup_magic_sword_type(type_roll)

        weapon_type = type_data["type"]
        damage_one = type_data.get("damage_one_hand")
        damage_two = type_data.get("damage_two_hands")

        if damage_one and damage_two:
            damage = f"{damage_one}/{damage_two}"
        elif damage_two:
            damage = damage_two
        else:
            damage = damage_one

        # 2. Schopnost meče (k10)
        sword_roll = random.randint(1, 10)
        sword_data = TableLoader.lookup_magic_sword(sword_roll)

        # 3. Prokletí (1/6 šance)
        curse_roll = roll_d6()
        cursed = (curse_roll == 1)
        curse_text = None
        curse_lift_text = None

        if cursed:
            curse_data = TableLoader.lookup_magic_sword_curse(curse_roll)
            if curse_data:
                curse_text = curse_data["curse"]
                curse_lift_text = curse_data["lift_condition"]

        # Vytvoř MagicSword objekt
        magic_sword = MagicSword(
            weapon_type=weapon_type,
            damage=damage,
            name=sword_data["name"],
            ability=sword_data["ability"],
            trigger=sword_data["trigger"],
            effect_type=sword_data["effect_type"],
            tags=sword_data.get("tags", []),
            usage_dots=3,
            cursed=cursed,
            curse=curse_text,
            curse_lift=curse_lift_text
        )

        # Vytvoř TreasureItem
        return TreasureItem(
            type="magic_sword",
            name=f"Kouzelný meč: {sword_data['name']}",
            description=f"{weapon_type} meč ({damage})",
            value=None,  # Kouzelné meče nemají pevnou cenu
            slots=1,
            usage_dots=3,
            magic_sword=magic_sword,
            notes=f"{'PROKLETÝ! ' if cursed else ''}{sword_data['ability']}"
        )

    @staticmethod
    def _generate_spell_item() -> TreasureItem:
        """
        Vygeneruj kouzlo jako TreasureItem.

        Použije SpellGenerator pro vytvoření kouzla, pak spočítá hodnotu (k6 × 100 ď).

        Returns:
            TreasureItem s Spell objektem
        """
        # Vygeneruj kouzlo pomocí SpellGenerator
        spell = SpellGenerator.create()

        # Hodnota plně nabitého kouzla: k6 × 100 ď
        value = roll_d6() * 100

        return TreasureItem(
            type="spell",
            name=f"Kouzlo: {spell.name}",
            description=spell.effect,
            value=value,
            slots=1,
            usage_dots=3,  # Plně nabité ○○○
            spell=spell,
            notes=f"Hodnota: {value} ď (plně nabité), Dobití: {spell.recharge}"
        )
