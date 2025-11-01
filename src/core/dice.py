"""
Dice rolling mechaniky
"""
import random
from typing import Tuple, List
from enum import Enum


class DiceType(Enum):
    """Typy kostek používané v Mausritter"""
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D66 = 66  # Speciální - hod 2d6 jako desítky a jednotky


def roll_d6() -> int:
    """Hod 1d6"""
    return random.randint(1, 6)


def roll_d8() -> int:
    """Hod 1d8"""
    return random.randint(1, 8)


def roll_d20() -> int:
    """Hod 1d20"""
    return random.randint(1, 20)


def roll_d66() -> int:
    """
    Hod d66 - speciální mechanika Mausritter
    První kostka = desítky, druhá = jednotky
    Výsledky: 11, 12, 13, ... 65, 66
    """
    tens = random.randint(1, 6) * 10
    ones = random.randint(1, 6)
    return tens + ones


def roll(dice: str) -> int:
    """
    Univerzální roller pro formát "XdY" nebo "dY"
    Např: "2d6", "d20", "3d4"
    """
    dice = dice.lower().strip()

    if dice == "d66":
        return roll_d66()

    # Parse formát XdY
    if 'd' not in dice:
        raise ValueError(f"Neplatný formát kostky: {dice}")

    parts = dice.split('d')
    if parts[0] == '':
        num_dice = 1
    else:
        num_dice = int(parts[0])

    die_size = int(parts[1])

    # Hod kostkami
    total = sum(random.randint(1, die_size) for _ in range(num_dice))
    return total


def roll_with_details(dice: str) -> Tuple[int, List[int]]:
    """
    Hod kostkou s detaily jednotlivých hodů
    Returns: (celkový součet, seznam jednotlivých hodů)
    """
    dice = dice.lower().strip()

    if dice == "d66":
        result = roll_d66()
        return result, [result]

    # Parse formát XdY
    if 'd' not in dice:
        raise ValueError(f"Neplatný formát kostky: {dice}")

    parts = dice.split('d')
    if parts[0] == '':
        num_dice = 1
    else:
        num_dice = int(parts[0])

    die_size = int(parts[1])

    # Hod kostkami
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(rolls)

    return total, rolls


def attribute_test(attribute_value: int, modifier: int = 0) -> Tuple[bool, int]:
    """
    Test vlastnosti - roll under mechanika
    Hod d20, musí být <= attribute_value + modifier

    Returns: (úspěch, hozená hodnota)
    """
    roll_result = roll_d20()
    target = attribute_value + modifier
    success = roll_result <= target

    return success, roll_result


def advantage_roll() -> int:
    """Hod s výhodou - hoď 2d20, vezmi lepší"""
    roll1 = roll_d20()
    roll2 = roll_d20()
    return min(roll1, roll2)  # Menší je lepší v roll-under systému


def disadvantage_roll() -> int:
    """Hod s nevýhodou - hoď 2d20, vezmi horší"""
    roll1 = roll_d20()
    roll2 = roll_d20()
    return max(roll1, roll2)  # Větší je horší v roll-under systému


def roll_3d6_keep_2() -> int:
    """
    Hod 3d6, vezmi 2 nejvyšší - pro generování vlastností

    Podle pravidel Mausritter: hod 3d6 a sečti 2 nejvyšší kostky.

    Returns:
        Součet 2 nejvyšších hodů (2-12)

    Example:
        >>> roll_3d6_keep_2()  # Např. hody [6, 4, 2] -> 6+4 = 10
        10
    """
    rolls = [roll_d6() for _ in range(3)]
    rolls.sort(reverse=True)
    return rolls[0] + rolls[1]
