"""Tests pro dice modul"""
import pytest
from src.core.dice import (
    roll_d6, roll_d20, roll_d66, roll,
    roll_with_details, attribute_test,
    advantage_roll, disadvantage_roll
)


def test_roll_d6():
    """Test hodu d6"""
    for _ in range(100):
        result = roll_d6()
        assert 1 <= result <= 6


def test_roll_d20():
    """Test hodu d20"""
    for _ in range(100):
        result = roll_d20()
        assert 1 <= result <= 20


def test_roll_d66():
    """Test hodu d66"""
    for _ in range(100):
        result = roll_d66()
        # Validní výsledky jsou 11-16, 21-26, ..., 61-66
        tens = result // 10
        ones = result % 10
        assert 1 <= tens <= 6
        assert 1 <= ones <= 6


def test_roll_format():
    """Test parsování formátu XdY"""
    # Test jednoduchých formátů
    for _ in range(20):
        result = roll("d6")
        assert 1 <= result <= 6

        result = roll("2d6")
        assert 2 <= result <= 12

        result = roll("3d4")
        assert 3 <= result <= 12


def test_roll_with_details():
    """Test hodu s detaily"""
    total, rolls = roll_with_details("3d6")
    assert len(rolls) == 3
    assert all(1 <= r <= 6 for r in rolls)
    assert total == sum(rolls)


def test_attribute_test():
    """Test attribute testu"""
    # Test s vysokou hodnotou - měl by téměř vždy uspět
    successes = sum(
        1 for _ in range(100)
        if attribute_test(attribute_value=18, modifier=0)[0]
    )
    assert successes > 80  # Očekáváme > 80% úspěšnost

    # Test s nízkou hodnotou - měl by často selhat
    successes = sum(
        1 for _ in range(100)
        if attribute_test(attribute_value=5, modifier=0)[0]
    )
    assert successes < 40  # Očekáváme < 40% úspěšnost


def test_advantage_roll():
    """Test hodu s výhodou"""
    for _ in range(20):
        result = advantage_roll()
        assert 1 <= result <= 20


def test_disadvantage_roll():
    """Test hodu s nevýhodou"""
    for _ in range(20):
        result = disadvantage_roll()
        assert 1 <= result <= 20
