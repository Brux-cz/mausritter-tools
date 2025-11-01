# -*- coding: utf-8 -*-
"""
Testy pro AdventureHookGenerator

Test coverage:
- Základní generování háčku
- Všechny háčky (1-6)
- Kategorie a emoji
- JSON konverze
- Otázky pro rozvíjení
"""

import json
from src.generators.adventure_hook import AdventureHookGenerator
from src.core.models import AdventureHook


def test_basic_generation():
    """Test základního generování háčku"""
    hook = AdventureHookGenerator.create()

    assert isinstance(hook, AdventureHook)
    assert hook.hook
    assert hook.category
    assert isinstance(hook.questions, list)
    assert 1 <= hook.roll <= 6


def test_hook_1_family():
    """Test háčku 1: Hledání ztraceného člena rodiny"""
    hook = AdventureHookGenerator.create(roll=1)

    assert hook.roll == 1
    assert hook.hook == "Hledání ztraceného člena rodiny"
    assert hook.category == "personal"
    assert hook.category_name_cz == "Osobní"
    assert hook.category_emoji == "👨‍👩‍👧‍👦"
    assert len(hook.questions) == 4
    assert "Kdo se ztratil?" in hook.questions


def test_hook_2_duty():
    """Test háčku 2: Vyšetřování na příkaz šlechtice"""
    hook = AdventureHookGenerator.create(roll=2)

    assert hook.roll == 2
    assert hook.hook == "Vyšetřování na příkaz myšího šlechtice"
    assert hook.category == "duty"
    assert hook.category_name_cz == "Povinnost"
    assert hook.category_emoji == "⚔️"
    assert len(hook.questions) == 4


def test_hook_3_quest():
    """Test háčku 3: Čaroděj potřebuje přísadu"""
    hook = AdventureHookGenerator.create(roll=3)

    assert hook.roll == 3
    assert hook.hook == "Myší čaroděj potřebuje přísadu do kouzla"
    assert hook.category == "quest"
    assert hook.category_name_cz == "Úkol"
    assert hook.category_emoji == "🔮"
    assert len(hook.questions) == 4


def test_hook_4_threat():
    """Test háčku 4: Tvor trápí osadu"""
    hook = AdventureHookGenerator.create(roll=4)

    assert hook.roll == 4
    assert hook.hook == "Místo je doupětem tvora, který trápí myší osadu"
    assert hook.category == "threat"
    assert hook.category_name_cz == "Hrozba"
    assert hook.category_emoji == "⚠️"
    assert len(hook.questions) == 4


def test_hook_5_treasure():
    """Test háčku 5: Mapa k pokladu"""
    hook = AdventureHookGenerator.create(roll=5)

    assert hook.roll == 5
    assert hook.hook == "Vede sem zděděná mapa k pokladu"
    assert hook.category == "treasure"
    assert hook.category_name_cz == "Poklad"
    assert hook.category_emoji == "💰"
    assert len(hook.questions) == 4


def test_hook_6_survival():
    """Test háčku 6: Útočiště před bouřkou"""
    hook = AdventureHookGenerator.create(roll=6)

    assert hook.roll == 6
    assert hook.hook == "Myši hledají útočiště před hroznou bouřkou"
    assert hook.category == "survival"
    assert hook.category_name_cz == "Přežití"
    assert hook.category_emoji == "🌪️"
    assert len(hook.questions) == 4


def test_all_hooks_have_questions():
    """Test že všechny háčky mají otázky pro rozvíjení"""
    for roll in range(1, 7):
        hook = AdventureHookGenerator.create(roll=roll)
        assert len(hook.questions) > 0, f"Háček {roll} nemá otázky"
        assert all(isinstance(q, str) for q in hook.questions), f"Háček {roll} má neplatné otázky"


def test_all_categories_unique():
    """Test že každý háček má unikátní kategorii"""
    categories = []
    for roll in range(1, 7):
        hook = AdventureHookGenerator.create(roll=roll)
        categories.append(hook.category)

    assert len(set(categories)) == 6, "Kategorie háčků nejsou unikátní"


def test_to_dict():
    """Test konverze na dictionary"""
    hook = AdventureHookGenerator.create(roll=1)
    data = AdventureHookGenerator.to_dict(hook)

    assert isinstance(data, dict)
    assert "hook" in data
    assert "category" in data
    assert "category_name" in data
    assert "questions" in data
    assert "roll" in data
    assert data["roll"] == 1
    assert data["category_name"] == "Osobní"


def test_to_json():
    """Test konverze na JSON"""
    hook = AdventureHookGenerator.create(roll=2)
    json_str = AdventureHookGenerator.to_json(hook)

    assert isinstance(json_str, str)
    data = json.loads(json_str)
    assert data["hook"] == "Vyšetřování na příkaz myšího šlechtice"
    assert data["category"] == "duty"
    assert data["roll"] == 2


def test_format_text():
    """Test textového formátování"""
    hook = AdventureHookGenerator.create(roll=3)
    text = AdventureHookGenerator.format_text(hook)

    assert isinstance(text, str)
    assert "HÁČEK DOBRODRUŽSTVÍ" in text
    assert hook.hook in text
    assert hook.category_name_cz in text
    assert "Otázky pro rozvíjení:" in text


def test_random_generation_produces_valid_hooks():
    """Test že náhodné generování produkuje validní háčky"""
    for _ in range(10):
        hook = AdventureHookGenerator.create()
        assert 1 <= hook.roll <= 6
        assert hook.hook
        assert hook.category
        assert len(hook.questions) > 0


def test_category_emoji_mapping():
    """Test že všechny kategorie mají správné emoji"""
    expected_emojis = {
        "personal": "👨‍👩‍👧‍👦",
        "duty": "⚔️",
        "quest": "🔮",
        "threat": "⚠️",
        "treasure": "💰",
        "survival": "🌪️",
    }

    for roll in range(1, 7):
        hook = AdventureHookGenerator.create(roll=roll)
        expected_emoji = expected_emojis.get(hook.category)
        assert hook.category_emoji == expected_emoji, f"Nesprávné emoji pro kategorii {hook.category}"


def test_category_name_cz_mapping():
    """Test že všechny kategorie mají české názvy"""
    expected_names = {
        "personal": "Osobní",
        "duty": "Povinnost",
        "quest": "Úkol",
        "threat": "Hrozba",
        "treasure": "Poklad",
        "survival": "Přežití",
    }

    for roll in range(1, 7):
        hook = AdventureHookGenerator.create(roll=roll)
        expected_name = expected_names.get(hook.category)
        assert hook.category_name_cz == expected_name, f"Nesprávný český název pro kategorii {hook.category}"
