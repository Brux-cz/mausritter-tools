"""
CLI rozhraní pro Mausritter Tools
"""
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from src.core.dice import roll, roll_with_details, attribute_test
from src.core.models import Character, NPC, Hireling, Weather, Reaction, Spell, TreasureHoard, TreasureItem, MagicSword, AdventureSeed, Tavern, Settlement, AdventureHook, CreatureVariant, Hex
from src.generators.character import CharacterGenerator
from src.generators.npc import NPCGenerator
from src.generators.hireling import HirelingGenerator
from src.generators.weather import WeatherGenerator
from src.generators.reaction import ReactionGenerator
from src.generators.spell import SpellGenerator
from src.generators.treasure import TreasureGenerator
from src.generators.adventure import AdventureSeedGenerator
from src.generators.tavern import TavernGenerator
from src.generators.settlement import SettlementGenerator
from src.generators.adventure_hook import AdventureHookGenerator
from src.generators.creature_variant import CreatureVariantGenerator
from src.generators.hex import HexGenerator

# Fix Windows console encoding for Czech characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Mausritter Tools - nástroje a generátory pro Mausritter TTRPG"""
    pass


@main.command()
@click.argument("dice", default="d20")
def roll_dice(dice: str):
    """
    Hoď kostkou

    Příklady:
        mausritter roll d20
        mausritter roll 2d6
        mausritter roll d66
    """
    try:
        total, rolls = roll_with_details(dice)

        console.print(f"[bold cyan]Hod {dice}:[/bold cyan]")
        if len(rolls) > 1:
            console.print(f"Jednotlivé hody: {rolls}")
        console.print(f"[bold green]Výsledek: {total}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}")


@main.command()
@click.argument("attribute", type=int)
@click.option("--modifier", "-m", default=0, help="Modifikátor testu")
def test(attribute: int, modifier: int):
    """
    Test vlastnosti (roll under d20)

    Příklad:
        mausritter test 12
        mausritter test 10 --modifier 2
    """
    success, roll_value = attribute_test(attribute, modifier)
    target = attribute + modifier

    console.print(f"[bold cyan]Test vlastnosti:[/bold cyan]")
    console.print(f"Cílové číslo: {target}")
    console.print(f"Hod: {roll_value}")

    if success:
        console.print(f"[bold green]ÚSPĚCH![/bold green] ({roll_value} <= {target})")
    else:
        console.print(f"[bold red]NEÚSPĚCH[/bold red] ({roll_value} > {target})")


@main.group()
def generate():
    """Generátory pro postavy, lokace, atd."""
    pass


@generate.command()
@click.option("--name", "-n", help="Vlastní jméno postavy")
@click.option("--gender", "-g", type=click.Choice(["male", "female"]), default="male", help="Pohlaví (pro správný tvar příjmení)")
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", "-s", type=click.Path(), help="Uložit do souboru")
def character(name: str, gender: str, output_json: bool, save: str):
    """
    Vygeneruj náhodnou myší postavu

    Příklady:
        mausritter generate character
        mausritter generate character --name "Pepřík"
        mausritter generate character --gender female
        mausritter generate character --json
        mausritter generate character --save postava.json
    """
    try:
        # Generuj postavu
        char = CharacterGenerator.create(name=name, gender=gender)

        if output_json:
            # JSON výstup
            output = CharacterGenerator.to_json(char)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_character(char)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(CharacterGenerator.to_json(char))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}", style="red")
        import traceback
        traceback.print_exc()


def display_character(char: Character):
    """
    Zobraz postavu v pěkném formátu s Rich formátováním.

    Args:
        char: Character instance k zobrazení
    """
    # Header - jméno a původ
    title = Text(char.name, style="bold cyan", justify="center")
    subtitle = Text(f"⭐ {char.background}", style="dim italic", justify="center")

    # Vlastnosti s vizuálními bary
    def make_bar(value: int, max_val: int = 12) -> str:
        """Vytvoř progress bar pro vlastnost"""
        filled = int((value / max_val) * 10)
        return "█" * filled + "░" * (10 - filled)

    attrs_text = f"""[bold]Vlastnosti:[/bold]
  Síla:      {char.strength:2d}  [{make_bar(char.strength)}]
  Mrštnost:  {char.dexterity:2d}  [{make_bar(char.dexterity)}]
  Vůle:      {char.willpower:2d}  [{make_bar(char.willpower)}]

[bold]Zdraví:[/bold]
  BO: {char.current_hp}/{char.max_hp}  {"❤️" * char.current_hp}

[bold]Počáteční výbava:[/bold]"""

    # Přidej inventář (jen vyplněné sloty)
    for i, item in enumerate(char.inventory):
        if item:
            attrs_text += f"\n  {i+1}. {item}"

    # Rodné znamení
    if char.birthsign:
        attrs_text += f"\n\n[bold]Rodné znamení:[/bold]\n  {char.birthsign}"

    # Srst
    if char.coat:
        attrs_text += f"\n\n[bold]Srst:[/bold]\n  {char.coat}"

    # Výrazný rys
    if char.appearance:
        attrs_text += f"\n\n[bold]Výrazný rys:[/bold]\n  {char.appearance}"

    # Poznámky (počáteční ďobky)
    if char.notes:
        attrs_text += f"\n\n[bold]Poznámky:[/bold]\n  {char.notes}"

    # Vytvoř panel
    panel = Panel(
        attrs_text,
        title=title,
        subtitle=subtitle,
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--name", "-n", help="Vlastní jméno NPC")
@click.option("--gender", "-g", type=click.Choice(["male", "female"]), default="male", help="Pohlaví (pro správný tvar příjmení)")
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", "-s", type=click.Path(), help="Uložit do souboru")
def npc(name: str, gender: str, output_json: bool, save: str):
    """
    Vygeneruj náhodné NPC (nehráčskou postavu)

    Příklady:
        mausritter generate npc
        mausritter generate npc --name "Pepřík"
        mausritter generate npc --gender female
        mausritter generate npc --json
        mausritter generate npc --save npc.json
    """
    try:
        # Generuj NPC
        npc_obj = NPCGenerator.create(name=name, gender=gender)

        if output_json:
            # JSON výstup
            output = NPCGenerator.to_json(npc_obj)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_npc(npc_obj)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(NPCGenerator.to_json(npc_obj))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}", style="red")
        import traceback
        traceback.print_exc()


def display_npc(npc_obj: NPC):
    """
    Zobraz NPC v pěkném formátu s Rich formátováním.

    Args:
        npc_obj: NPC instance k zobrazení
    """
    # Header - jméno
    title = Text(npc_obj.name, style="bold magenta", justify="center")
    subtitle = Text(f"🎭 {npc_obj.social_status}", style="dim italic", justify="center")

    # Sestavení textu
    npc_text = f"""[bold]Rodné znamení:[/bold]
  {npc_obj.birthsign}

[bold]Vzhled:[/bold]
  {npc_obj.appearance}

[bold]Zvláštnost:[/bold]
  {npc_obj.quirk}

[bold]Po čem touží:[/bold]
  {npc_obj.desire}

[bold]Vztah k jiné myši:[/bold]
  {npc_obj.relationship}

[bold]Reakce při setkání:[/bold]
  {npc_obj.reaction}"""

    # Platba za služby
    if npc_obj.payment:
        npc_text += f"\n\n[bold]Platba za služby:[/bold]\n  {npc_obj.payment}"

    # Poznámky
    if npc_obj.notes:
        npc_text += f"\n\n[bold]Poznámky:[/bold]\n  {npc_obj.notes}"

    # Vytvoř panel
    panel = Panel(
        npc_text,
        title=title,
        subtitle=subtitle,
        border_style="magenta",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--type", "-t", "hireling_type", type=click.IntRange(1, 9), help="ID typu pomocníka (1-9)")
@click.option("--name", "-n", help="Vlastní jméno pomocníka")
@click.option("--gender", "-g", type=click.Choice(["male", "female"]), default="male", help="Pohlaví (pro správný tvar příjmení)")
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", "-s", type=click.Path(), help="Uložit do souboru")
def hireling(hireling_type: int, name: str, gender: str, output_json: bool, save: str):
    """
    Vygeneruj náhodného pomocníka (hireling)

    Příklady:
        python -m src.cli generate hireling
        python -m src.cli generate hireling --type 6
        python -m src.cli generate hireling --name "Válečník"
        python -m src.cli generate hireling --gender female
        python -m src.cli generate hireling --json
        python -m src.cli generate hireling --save pomocnik.json
    """
    try:
        # Generuj pomocníka
        hireling_obj, availability = HirelingGenerator.create(
            type_id=hireling_type,
            name=name,
            gender=gender
        )

        if output_json:
            # JSON výstup
            output = HirelingGenerator.to_json(hireling_obj)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_hireling(hireling_obj, availability)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(HirelingGenerator.to_json(hireling_obj))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}", style="red")
        import traceback
        traceback.print_exc()


def display_hireling(hireling_obj: Hireling, availability: int):
    """Zobraz pomocníka v pěkném formátu"""

    # Header - jméno
    title = Text(hireling_obj.name, style="bold yellow", justify="center")
    subtitle = Text(f"⚔️ {hireling_obj.type}", style="dim", justify="center")

    # Vlastnosti a inventář
    hireling_text = f"""[bold]Denní mzda:[/bold] {hireling_obj.daily_wage} ď

[bold]⚔️ Vlastnosti:[/bold]
  Síla:      {hireling_obj.strength:2d}
  Mrštnost:  {hireling_obj.dexterity:2d}
  Vůle:      {hireling_obj.willpower:2d}
  BO:        {hireling_obj.hp}/{hireling_obj.hp}

[bold]🎒 Inventář:[/bold]
  [   ] [   ] [   ]    (packy + tělo)
  [   ] [   ] [   ]    (batoh)

[bold]📊 Postup:[/bold]
  Level: {hireling_obj.level}  |  XP: {hireling_obj.experience}/1000
  Morálka: {hireling_obj.morale}

[bold]📍 Dostupnost:[/bold]
  {availability} {'pomocník' if availability == 1 else 'pomocníci' if availability < 5 else 'pomocníků'} tohoto typu {'je' if availability == 1 else 'jsou'} k dispozici"""

    # Poznámky (popis typu)
    if hireling_obj.notes:
        hireling_text += f"\n\n[bold]Poznámky:[/bold]\n  {hireling_obj.notes}"

    # Vytvoř panel
    panel = Panel(
        hireling_text,
        title=title,
        subtitle=subtitle,
        border_style="yellow",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--season", "-s", type=click.Choice(["spring", "summer", "autumn", "winter"]), default="spring", help="Roční období")
@click.option("--with-event", "-e", is_flag=True, help="Zahrnout sezónní událost")
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", type=click.Path(), help="Uložit do souboru")
def weather(season: str, with_event: bool, output_json: bool, save: str):
    """
    Vygeneruj počasí pro dané roční období

    Příklady:
        python -m src.cli generate weather
        python -m src.cli generate weather --season winter
        python -m src.cli generate weather --season autumn --with-event
        python -m src.cli generate weather --json
        python -m src.cli generate weather --save weather.json
    """
    try:
        # Generuj počasí
        weather_obj = WeatherGenerator.create(season=season, with_event=with_event)

        if output_json:
            # JSON výstup
            output = WeatherGenerator.to_json(weather_obj)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_weather(weather_obj)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(WeatherGenerator.to_json(weather_obj))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[bold red]Chyba:[/bold red] {e}", style="red")
        import traceback
        traceback.print_exc()


def display_weather(weather_obj: Weather):
    """Zobraz počasí v pěkném formátu"""

    # Emoji pro sezóny
    season_emoji = {
        "spring": "🌸",
        "summer": "☀️",
        "autumn": "🍂",
        "winter": "❄️"
    }

    # Získej český název sezóny
    season_name = WeatherGenerator.get_season_name(weather_obj.season)
    emoji = season_emoji.get(weather_obj.season, "🌤️")

    # Header
    title = Text(f"{emoji} {season_name}", style="bold green", justify="center")

    # Počasí
    weather_text = f"[bold]Počasí:[/bold] {weather_obj.weather}"

    # Varování pokud je nepříznivé
    if weather_obj.unfavorable:
        weather_text += "\n\n[bold red]⚠️  NEPŘÍZNIVÉ pro cestování[/bold red]"
        weather_text += "\n\nKaždá myš musí při cestování uspět v [bold]záchraně na sílu[/bold]"
        weather_text += "\nkaždou hlídku, jinak dostane stav [bold]Vyčerpání[/bold]."

    # Sezónní událost (pokud je)
    if weather_obj.event:
        weather_text += f"\n\n[bold]Sezónní událost:[/bold]\n{weather_obj.event}"

    # Vytvoř panel
    panel = Panel(
        weather_text,
        title=title,
        border_style="green" if not weather_obj.unfavorable else "red",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--modifier", "-m", type=int, default=0, help="Modifikátor k hodu (např. +1 za dárek, -1 za agresi)")
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", type=click.Path(), help="Uložit do souboru")
def reaction(modifier: int, output_json: bool, save: str):
    """
    Vygeneruj reakci NPC/tvora při setkání

    Hoď 2k6 a urči počáteční dispozici tvora k hráčským postavám.
    Použij modifikátory podle kontextu:
      +1 pokud myši přinesly dárek
      -1 pokud jsou agresivní nebo rušivé
      -2 pokud tvor byl nedávno napaden

    Příklady:
        python -m src.cli generate reaction
        python -m src.cli generate reaction --modifier 1
        python -m src.cli generate reaction -m -2
        python -m src.cli generate reaction --json
        python -m src.cli generate reaction --save reaction.json
    """
    import traceback
    try:
        # Generuj reakci
        reaction_obj = ReactionGenerator.create(modifier=modifier)

        if output_json:
            # JSON výstup
            output = ReactionGenerator.to_json(reaction_obj)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_reaction(reaction_obj)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(ReactionGenerator.to_json(reaction_obj))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[red]Chyba při generování reakce: {e}[/red]")
        traceback.print_exc()


def display_reaction(reaction_obj: Reaction):
    """Zobraz reakci v pěkném formátu"""

    # Barvy pro různé reakce
    color = ReactionGenerator.get_reaction_color(reaction_obj.reaction)

    # Emoji podle reakce
    reaction_emoji = {
        "Agresivní": "⚔️",
        "Nepřátelská": "😠",
        "Nejistá": "🤔",
        "Povídavá": "😊",
        "Nápomocná": "💚"
    }
    emoji = reaction_emoji.get(reaction_obj.reaction, "❓")

    # Header
    title = Text(f"{emoji} Reakce NPC", style=f"bold {color}", justify="center")

    # Obsah
    content_parts = []
    content_parts.append(f"[bold]Hod:[/bold] {reaction_obj.roll} (2k6)")
    content_parts.append(f"\n[bold]Reakce:[/bold] [{color}]{reaction_obj.reaction}[/{color}]")
    content_parts.append(f"\n\n[bold]GM otázka:[/bold]\n[italic]{reaction_obj.question}[/italic]")

    # Poznámky (pokud jsou)
    if reaction_obj.notes:
        content_parts.append(f"\n\n[dim]{reaction_obj.notes}[/dim]")

    # Tip pro GM
    content_parts.append("\n\n[dim]💡 Tip: Toto je počáteční dispozice, může se změnit podle chování hráčů.[/dim]")

    reaction_text = "".join(content_parts)

    # Vytvoř panel
    panel = Panel(
        reaction_text,
        title=title,
        border_style=color,
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--json", "-j", "output_json", is_flag=True, help="Výstup jako JSON")
@click.option("--save", type=click.Path(), help="Uložit do souboru")
def spell(output_json: bool, save: str):
    """
    Vygeneruj náhodné kouzlo

    Hoď 2d8 a urči náhodné kouzlo z tabulky kouzel Mausritter.
    Každé kouzlo má efekt s placeholdery [POČET] a [SOUČET] pro sesílání,
    plus podmínku dobití.

    Příklady:
        python -m src.cli generate spell
        python -m src.cli generate spell --json
        python -m src.cli generate spell --save kouzlo.json
    """
    import traceback
    try:
        # Generuj kouzlo
        spell_obj = SpellGenerator.create()

        if output_json:
            # JSON výstup
            output = SpellGenerator.to_json(spell_obj)
            console.print(output)
        else:
            # Pěkný formátovaný výstup
            display_spell(spell_obj)

        # Uložení do souboru
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(SpellGenerator.to_json(spell_obj))
            console.print(f"\n[green]✓[/green] Uloženo do {save}")

    except Exception as e:
        console.print(f"[red]Chyba při generování kouzla: {e}[/red]")
        traceback.print_exc()


def display_spell(spell_obj: Spell):
    """Zobraz kouzlo v pěkném formátu"""

    # Barva podle kategorie
    color = SpellGenerator.get_spell_color(spell_obj.tags)
    category = SpellGenerator.get_spell_category(spell_obj.tags)

    # Header
    title = Text(f"✨ {spell_obj.name}", style=f"bold {color}", justify="center")

    # Obsah
    content_parts = []
    content_parts.append(f"[bold]Hod:[/bold] {spell_obj.roll} (2d8)")
    content_parts.append(f"[bold]Kategorie:[/bold] {category}")

    content_parts.append(f"\n[bold]Efekt:[/bold]")
    content_parts.append(f"{spell_obj.effect}")

    content_parts.append(f"\n[bold]Dobití:[/bold]")
    content_parts.append(f"{spell_obj.recharge}")

    # Vysvětlení placeholderů
    content_parts.append("\n[dim]💡 [POČET] = počet kostek při sesílání, [SOUČET] = součet hodnot[/dim]")
    content_parts.append("[dim]   Kouzlo má 3 tečky použití (●●●) když je plně nabité[/dim]")

    spell_text = "\n".join(content_parts)

    # Vytvoř panel
    panel = Panel(
        spell_text,
        title=title,
        border_style=color,
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")


@generate.command()
@click.option("--bonus", "-b", default=0, type=int, help="Počet bonusových hodů k20 (0-4)")
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
def treasure(bonus: int, output_json: bool, save: str):
    """
    Vygeneruj poklad (hoard).

    Bonusové hody (0-4) za kladné odpovědi na otázky:
    - Je v bývalé myší osadě / hradě / jeskyni? (+1)
    - Je ve vysoce magické oblasti? (+1)
    - Brání ho velké zvíře / záludná past? (+1)
    - Překonaly myši velké nesnáze? (+1)

    Příklady:
    \b
        python -m src.cli generate treasure
        python -m src.cli generate treasure --bonus 2
        python -m src.cli generate treasure -b 4 --json
    """
    if bonus < 0 or bonus > 4:
        console.print("[red]Chyba: Bonusové hody musí být 0-4[/red]")
        return

    # Vygeneruj poklad
    hoard = TreasureGenerator.create(bonus_rolls=bonus)

    # JSON výstup
    if output_json:
        import json
        hoard_dict = {
            "total_rolls": hoard.total_rolls,
            "bonus_rolls": hoard.bonus_rolls,
            "total_value": hoard.total_value,
            "items": []
        }

        for item in hoard.items:
            item_dict = {
                "type": item.type,
                "name": item.name,
                "description": item.description,
                "value": item.value,
                "slots": item.slots,
                "usage_dots": item.usage_dots,
                "quantity": item.quantity,
                "notes": item.notes
            }

            # Přidej speciální objekty pokud existují
            if item.spell:
                item_dict["spell"] = {
                    "roll": item.spell.roll,
                    "name": item.spell.name,
                    "effect": item.spell.effect,
                    "recharge": item.spell.recharge,
                    "tags": item.spell.tags
                }

            if item.magic_sword:
                item_dict["magic_sword"] = {
                    "weapon_type": item.magic_sword.weapon_type,
                    "damage": item.magic_sword.damage,
                    "name": item.magic_sword.name,
                    "ability": item.magic_sword.ability,
                    "trigger": item.magic_sword.trigger,
                    "cursed": item.magic_sword.cursed,
                    "curse": item.magic_sword.curse,
                    "curse_lift": item.magic_sword.curse_lift
                }

            hoard_dict["items"].append(item_dict)

        json_output = json.dumps(hoard_dict, ensure_ascii=False, indent=2)
        console.print(json_output)

        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")

        return

    # Normální výstup
    display_treasure(hoard)

    if save:
        import json
        # Stejný JSON export jako výše
        pass


def display_treasure(hoard: TreasureHoard):
    """
    Zobrazí poklad v terminálu s barevným formátováním.
    """
    # Hlavička
    title = f"💰 Poklad ({hoard.total_rolls}× k20)"
    if hoard.bonus_rolls > 0:
        title += f" [+{hoard.bonus_rolls} bonusové hody]"

    console.print("\n")
    console.print(Panel(
        f"[bold yellow]Celková hodnota: {hoard.total_value} ď[/bold yellow]\n"
        f"[dim]Položek: {len(hoard.items)}[/dim]",
        title=title,
        border_style="yellow",
        padding=(1, 2)
    ))
    console.print("\n")

    # Zobraz každou položku
    for i, item in enumerate(hoard.items, 1):
        display_treasure_item(item, i)


def display_treasure_item(item: TreasureItem, index: int):
    """
    Zobrazí jednu položku pokladu.
    """
    # Určí barvu podle typu
    color = get_treasure_color(item.type)
    icon = get_treasure_icon(item.type)

    # Název
    title = f"{icon} {index}. {item.name}"

    # Obsah panelu
    lines = []

    # Popis
    if item.description:
        lines.append(f"[dim]{item.description}[/dim]")
        lines.append("")

    # Hodnota
    if item.value is not None:
        lines.append(f"💰 Hodnota: [bold yellow]{item.value} ď[/bold yellow]")
    else:
        lines.append(f"💰 Hodnota: [dim]Neprodejné / neurčeno[/dim]")

    # Políčka
    if item.slots > 0:
        slots_str = "□" * item.slots
        lines.append(f"📦 Políčka: {slots_str} ({item.slots})")
    else:
        lines.append(f"📦 Políčka: [dim]Nezabírá místo[/dim]")

    # Tečky použití
    if item.usage_dots > 0:
        dots_str = "○" * item.usage_dots
        lines.append(f"🔘 Použití: {dots_str}")

    # Množství
    if item.quantity > 1:
        lines.append(f"🔢 Množství: {item.quantity}×")

    # Kupec (pro neobvyklý poklad)
    if item.buyer:
        lines.append(f"🏪 Kupec: [cyan]{item.buyer}[/cyan]")

    # Speciální objekty
    if item.spell:
        lines.append("")
        lines.append(f"✨ [bold magenta]KOUZLO[/bold magenta]")
        lines.append(f"Efekt: {item.spell.effect}")
        lines.append(f"[dim]Dobití: {item.spell.recharge}[/dim]")

    if item.magic_sword:
        lines.append("")
        lines.append(f"⚔️ [bold red]KOUZELNÝ MEČ[/bold red]")
        lines.append(f"Typ: {item.magic_sword.weapon_type} ({item.magic_sword.damage})")
        lines.append(f"Schopnost: {item.magic_sword.ability}")
        if item.magic_sword.cursed:
            lines.append("")
            lines.append(f"💀 [bold red]PROKLETÝ![/bold red]")
            lines.append(f"Kletba: {item.magic_sword.curse}")
            lines.append(f"Sejmutí: {item.magic_sword.curse_lift}")

    # Poznámky
    if item.notes:
        lines.append("")
        lines.append(f"📝 {item.notes}")

    content = "\n".join(lines)

    panel = Panel(
        content,
        title=title,
        border_style=color,
        padding=(1, 2)
    )

    console.print(panel)
    console.print("")


def get_treasure_color(treasure_type: str) -> str:
    """Vrátí barvu pro daný typ pokladu."""
    colors = {
        "pips": "yellow",           # 💰 Ďobky
        "magic_sword": "red",        # ⚔️ Kouzelný meč
        "spell": "magenta",          # ✨ Kouzlo
        "valuable": "blue",          # 💎 Cenný poklad
        "bulky": "cyan",             # 📦 Objemný poklad
        "unusual": "green",          # 🔮 Neobvyklý poklad
        "useful": "white",           # 🛠️ Užitečný poklad
        "trinket": "magenta",        # 🎁 Drobnost
        "supplies": "green",
        "torches": "yellow",
        "weapon": "red",
        "armor": "blue",
        "tool": "white",
        "hireling": "cyan"
    }
    return colors.get(treasure_type, "white")


def get_treasure_icon(treasure_type: str) -> str:
    """Vrátí emoji ikonu pro daný typ pokladu."""
    icons = {
        "pips": "💰",
        "magic_sword": "⚔️",
        "spell": "✨",
        "valuable": "💎",
        "bulky": "📦",
        "unusual": "🔮",
        "useful": "🛠️",
        "trinket": "🎁",
        "supplies": "🍞",
        "torches": "🔥",
        "weapon": "🗡️",
        "armor": "🛡️",
        "tool": "🔧",
        "hireling": "🐭"
    }
    return icons.get(treasure_type, "📜")


@generate.command()
@click.option("--custom", "-c", is_flag=True, help="Hoď na každý sloupec zvlášť (custom kombinace)")
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
@click.option("--inspiration", "-i", is_flag=True, help="Zobraz inspirační text pro GM")
def adventure(custom: bool, output_json: bool, save: str, inspiration: bool):
    """
    Vygeneruj semínko dobrodružství.

    Kombinuje Tvora, Problém a Komplikaci pro inspiraci při tvorbě questů.

    Příklady:
    \b
        python -m src.cli generate adventure
        python -m src.cli generate adventure --custom
        python -m src.cli generate adventure --inspiration
        python -m src.cli generate adventure --json
    """
    # Vygeneruj semínko
    if custom:
        seed = AdventureSeedGenerator.create_custom()
    else:
        seed = AdventureSeedGenerator.create()

    # JSON výstup
    if output_json:
        json_output = AdventureSeedGenerator.to_json(seed)
        console.print(json_output)

        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")

        return

    # Normální výstup
    display_adventure_seed(seed, show_inspiration=inspiration)

    if save:
        # Ulož jako JSON
        json_output = AdventureSeedGenerator.to_json(seed)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_adventure_seed(seed: AdventureSeed, show_inspiration: bool = False):
    """
    Zobrazí semínko dobrodružství v terminálu s barevným formátováním.

    Args:
        seed: AdventureSeed instance
        show_inspiration: Pokud True, zobrazí inspirační text pro GM
    """
    # Hlavička
    if seed.roll > 0:
        title = f"🎲 Semínko dobrodružství (k66: {seed.roll})"
    else:
        title = "🎲 Semínko dobrodružství (Custom kombinace)"

    # Obsah panelu
    lines = []

    # Tvor
    lines.append(f"[bold cyan]🎭 Tvor:[/bold cyan]")
    lines.append(f"   {seed.creature}")
    lines.append("")

    # Problém
    lines.append(f"[bold yellow]⚠️  Problém:[/bold yellow]")
    lines.append(f"   {seed.problem}")
    lines.append("")

    # Komplikace
    lines.append(f"[bold red]💥 Komplikace:[/bold red]")
    lines.append(f"   {seed.complication}")

    # Poznámky
    if seed.notes and not seed.notes.startswith("Custom"):
        lines.append("")
        lines.append(f"[dim]📝 {seed.notes}[/dim]")

    content = "\n".join(lines)

    panel = Panel(
        content,
        title=title,
        border_style="green",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")

    # Zobraz inspirační text pokud je požadováno
    if show_inspiration:
        inspiration_text = AdventureSeedGenerator.get_inspiration_text(seed)

        # Rozdel na řádky a obarvuj
        insp_lines = []
        for line in inspiration_text.split("\n"):
            if line.startswith("💡"):
                insp_lines.append(f"[bold magenta]{line}[/bold magenta]")
            elif line.startswith("KDO:") or line.startswith("CO:") or line.startswith("JAK:"):
                insp_lines.append(f"[bold cyan]{line}[/bold cyan]")
            elif line.startswith("❓"):
                insp_lines.append(f"[bold yellow]{line}[/bold yellow]")
            elif line.startswith("  →") or line.startswith("  -"):
                insp_lines.append(f"[dim]{line}[/dim]")
            else:
                insp_lines.append(line)

        inspiration_panel = Panel(
            "\n".join(insp_lines),
            title="💡 Inspirace pro GM",
            border_style="magenta",
            padding=(1, 2)
        )

        console.print(inspiration_panel)
        console.print("\n")


@generate.command()
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
def tavern(output_json: bool, save: str):
    """
    Vygeneruj hospodu/hostinec.

    Hospody se objevují ve vískách a větších osadách.
    Poskytují jídlo, pití a přístřeší pro místní i pocestné.

    Generuje:
    - Název (2× k12): "U [Přídavné jméno] [Podstatné jméno]"
    - Specialita (k12): Pokrm nebo nápoj
    """
    tavern_obj = TavernGenerator.create()

    if output_json:
        json_output = TavernGenerator.to_json(tavern_obj)
        console.print(json_output)
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")
        return

    display_tavern(tavern_obj)

    if save:
        json_output = TavernGenerator.to_json(tavern_obj)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_tavern(tavern: Tavern):
    """Zobraz hospodu v terminálu s barevným formátováním."""

    # Panel s názvem hospody
    name_panel = Panel(
        f"[bold yellow]{tavern.full_name}[/bold yellow]",
        title="🏠 HOSPODA",
        title_align="left",
        border_style="yellow",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(name_panel)

    # Specialita
    specialty_text = Text()
    specialty_text.append("🍲 Specialita: ", style="bold cyan")
    specialty_text.append(tavern.specialty, style="white")

    console.print(specialty_text)
    console.print()

    # Hody
    rolls_text = Text()
    rolls_text.append("🎲 Hody: ", style="dim")
    rolls_text.append(f"{tavern.roll_part1}/{tavern.roll_part2} ", style="dim cyan")
    rolls_text.append("(název), ", style="dim")
    rolls_text.append(f"{tavern.roll_specialty} ", style="dim cyan")
    rolls_text.append("(specialita)", style="dim")

    console.print(rolls_text)
    console.print("\n")


@generate.command()
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
@click.option("--name", "generate_name", is_flag=True, help="Vygeneruj název osady")
@click.option("--no-tavern", "no_tavern", is_flag=True, help="Negeneruj hospodu (i pro větší osady)")
def settlement(output_json: bool, save: str, generate_name: bool, no_tavern: bool):
    """
    Vygeneruj osadu (settlement).

    Osady jsou místa kde myši žijí, obchodují a odpočívají.
    Velikost osady určuje dostupné služby a prvky.

    Generuje:
    - Velikost (2d6 keep-lower): 1-6 (Farma → Velkoměsto)
    - Vláda (k6 + velikost): Typ správy osady
    - Detail (k20): Charakteristický rys
    - Řemesla (k20): 1× pro malé osady, 2× pro města
    - Prvky (k20): 1× pro osady, 2× pro velkoměsta
    - Událost (k20): Co se děje při příjezdu
    - Hospoda: Pro vísku a větší osady (použij --no-tavern pro vypnutí)
    - Název (--name): Volitelný název z tabulky semínek
    """
    settlement_obj = SettlementGenerator.create(
        generate_name=generate_name,
        generate_tavern=not no_tavern
    )

    if output_json:
        json_output = SettlementGenerator.to_json(settlement_obj)
        console.print(json_output)
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")
        return

    display_settlement(settlement_obj)

    if save:
        json_output = SettlementGenerator.to_json(settlement_obj)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_settlement(settlement: Settlement):
    """Zobraz osadu v terminálu s barevným formátováním."""

    # Hlavní nadpis
    title_text = "🏘️  OSADA"
    if settlement.name:
        title_text += f": {settlement.name}"

    main_panel = Panel(
        f"[bold cyan]{settlement.size_name}[/bold cyan]\n[white]{settlement.population}[/white]",
        title=title_text,
        title_align="left",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(main_panel)

    # Vláda a detail
    gov_text = Text()
    gov_text.append("⚖️  Vláda: ", style="bold magenta")
    gov_text.append(settlement.government, style="white")
    console.print(gov_text)

    detail_text = Text()
    detail_text.append("🔍 Detail: ", style="bold blue")
    detail_text.append(settlement.detail, style="white")
    console.print(detail_text)
    console.print()

    # Řemesla
    if settlement.trades:
        console.print("[bold yellow]🛠️  Řemesla:[/bold yellow]")
        for trade in settlement.trades:
            console.print(f"   • {trade}", style="white")
        console.print()

    # Prvky
    if settlement.features:
        console.print("[bold green]🏛️  Prvky:[/bold green]")
        for feature in settlement.features:
            console.print(f"   • {feature}", style="white")
        console.print()

    # Událost
    event_text = Text()
    event_text.append("📅 Událost: ", style="bold red")
    event_text.append(settlement.event, style="white")
    console.print(event_text)

    # Hospoda
    if settlement.tavern:
        console.print()
        tavern_panel = Panel(
            f"[bold yellow]{settlement.tavern.full_name}[/bold yellow]\n🍲 [cyan]{settlement.tavern.specialty}[/cyan]",
            title="🏠 Hospoda",
            title_align="left",
            border_style="yellow",
            padding=(0, 2)
        )
        console.print(tavern_panel)

    # Hody
    console.print()
    rolls_text = Text()
    rolls_text.append("🎲 Hody: ", style="dim")
    size_roll = f"{settlement.roll_size_die1},{settlement.roll_size_die2}→{min(settlement.roll_size_die1, settlement.roll_size_die2)}"
    rolls_text.append(size_roll, style="dim cyan")
    rolls_text.append(" (velikost), ", style="dim")
    rolls_text.append(f"{settlement.roll_government}", style="dim cyan")
    rolls_text.append(" (vláda), ", style="dim")
    rolls_text.append(f"{settlement.roll_detail}", style="dim cyan")
    rolls_text.append(" (detail)", style="dim")

    console.print(rolls_text)
    console.print("\n")


@generate.command()
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
def hook(output_json: bool, save: str):
    """
    Vygeneruj háček dobrodružství.

    Háček poskytuje důvod, proč se myši vydají na dobrodružství.
    Používá se pro motivaci hráčů na začátku kampaně nebo sezení.

    Generuje:
    - Háček (k6): Typ motivace (rodina, povinnost, úkol, hrozba, poklad, přežití)
    - Kategorie: Pro filtrování a organizaci
    - Otázky: Inspirační otázky pro rozvíjení příběhu

    Příklady:
    - Hledání ztraceného člena rodiny
    - Vyšetřování na příkaz šlechtice
    - Čaroděj potřebuje přísadu do kouzla
    """
    hook_obj = AdventureHookGenerator.create()

    if output_json:
        json_output = AdventureHookGenerator.to_json(hook_obj)
        console.print(json_output)
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")
        return

    display_adventure_hook(hook_obj)

    if save:
        json_output = AdventureHookGenerator.to_json(hook_obj)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_adventure_hook(hook: AdventureHook):
    """Zobraz háček dobrodružství v terminálu s barevným formátováním."""

    # Hlavní panel s háčkem
    title_text = f"{hook.category_emoji}  HÁČEK DOBRODRUŽSTVÍ"

    main_panel = Panel(
        f"[bold cyan]{hook.hook}[/bold cyan]",
        title=title_text,
        title_align="left",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(main_panel)

    # Kategorie
    category_text = Text()
    category_text.append("📋 Kategorie: ", style="bold magenta")
    category_text.append(hook.category_name_cz, style="white")
    console.print(category_text)
    console.print()

    # Otázky pro rozvíjení
    if hook.questions:
        console.print("[bold yellow]❓ Otázky pro rozvíjení:[/bold yellow]")
        for question in hook.questions:
            console.print(f"   • {question}", style="white")
        console.print()

    # Hod
    rolls_text = Text()
    rolls_text.append("🎲 Hod: ", style="dim")
    rolls_text.append(f"{hook.roll}", style="dim cyan")
    rolls_text.append(" (k6)", style="dim")

    console.print(rolls_text)
    console.print("\n")


@generate.command()
@click.argument("creature_type", type=click.Choice([
    "ghost", "snake", "cat", "rat", "mouse", "spider",
    "owl", "centipede", "fairy", "crow", "frog"
], case_sensitive=False))
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
def creature(creature_type: str, output_json: bool, save: str):
    """
    Vygeneruj variantu stvoření.

    Generuje specifické varianty různých stvoření podle oficiálních pravidel.
    Každý typ stvoření má 6 unikátních variant (k6).

    CREATURE_TYPE: Typ stvoření k vygenerování

    Dostupné typy:
    - ghost: Přízračné schopnosti
    - snake: Zvláštní hadi
    - cat: Kočičí pánové a paní
    - rat: Krysí gangy
    - mouse: Konkurenční myší dobrodruzi
    - spider: Druhy pavouků
    - owl: Soví čarodějové
    - centipede: Zevlující stonožky
    - fairy: Vílí plány
    - crow: Vraní písně
    - frog: Potulní žabí rytíři

    Příklady:
        mausritter generate creature ghost
        mausritter generate creature snake --json
        mausritter generate creature owl --save owl_wizard.json
    """
    creature_type_lower = creature_type.lower()
    variant_obj = CreatureVariantGenerator.create(creature_type_lower)

    if output_json:
        json_output = CreatureVariantGenerator.to_json(variant_obj)
        console.print(json_output)
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")
        return

    display_creature_variant(variant_obj)

    if save:
        json_output = CreatureVariantGenerator.to_json(variant_obj)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_creature_variant(variant: CreatureVariant):
    """Zobraz variantu stvoření v terminálu s barevným formátováním."""

    # Hlavní panel s variantou
    title_text = f"{variant.creature_emoji}  {variant.variant_table_name_cz.upper()}"

    main_panel = Panel(
        f"[bold cyan]{variant.name}[/bold cyan]",
        title=title_text,
        title_align="left",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(main_panel)

    # Typ stvoření
    type_text = Text()
    type_text.append("📋 Typ: ", style="bold magenta")
    type_text.append(variant.creature_name_cz, style="white")
    console.print(type_text)
    console.print()

    # Popis varianty
    console.print("[bold yellow]📝 Popis:[/bold yellow]")
    console.print(f"   {variant.description}", style="white")
    console.print()

    # Hod
    rolls_text = Text()
    rolls_text.append("🎲 Hod: ", style="dim")
    rolls_text.append(f"{variant.roll}", style="dim cyan")
    rolls_text.append(" (k6)", style="dim")

    console.print(rolls_text)
    console.print("\n")


@generate.command()
@click.option("--json", "output_json", is_flag=True, help="Výstup v JSON formátu")
@click.option("--save", type=str, help="Ulož do souboru")
@click.option("--with-settlement", is_flag=True, help="Vygeneruj hex s myší osadou")
def hex(output_json: bool, save: str, with_settlement: bool):
    """
    Vygeneruj hex pro hexcrawl kampaň.

    Generuje náhodný hex s typem a výrazným prvkem podle oficiálních pravidel.
    Každý hex má typ (Otevřená krajina, Les, Řeka, Lidské město) a detail
    s háčkem pro rozvíjení příběhu.

    Speciální: Hexy s kategorií "Myší osada" automaticky generují celou osadu
    pomocí Settlement Generatoru.

    Příklady:
        mausritter generate hex
        mausritter generate hex --with-settlement
        mausritter generate hex --json
        mausritter generate hex --save muj_hex.json
    """
    # Vygeneruj hex
    if with_settlement:
        hex_obj = HexGenerator.create_with_settlement()
    else:
        hex_obj = HexGenerator.create()

    if output_json:
        json_output = HexGenerator.to_json(hex_obj)
        console.print(json_output)
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(json_output)
            console.print(f"\n[green]Uloženo do {save}[/green]")
        return

    display_hex(hex_obj)

    if save:
        json_output = HexGenerator.to_json(hex_obj)
        with open(save, 'w', encoding='utf-8') as f:
            f.write(json_output)
        console.print(f"\n[green]Uloženo do {save}[/green]")


def display_hex(hex_obj: Hex):
    """Zobraz hex v terminálu s barevným formátováním."""

    # Hlavní panel s typem hexu
    title_text = f"{hex_obj.type_emoji}  HEX PRO HEXCRAWL"

    main_panel = Panel(
        f"[bold cyan]{hex_obj.type}[/bold cyan]",
        title=title_text,
        title_align="left",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(main_panel)

    # Kategorie detailu
    category_text = Text()
    category_text.append("📋 Kategorie: ", style="bold magenta")
    category_text.append(hex_obj.category_name_cz, style="white")
    console.print(category_text)
    console.print()

    # Detail
    console.print("[bold yellow]🔍 Detail:[/bold yellow]")
    console.print(f"   {hex_obj.detail_name}", style="white")
    console.print()

    # Háček
    console.print("[bold yellow]❓ Háček:[/bold yellow]")
    console.print(f"   {hex_obj.detail_hook}", style="dim white")
    console.print()

    # Pokud obsahuje settlement, zobraz settlement info
    if hex_obj.is_settlement and hex_obj.settlement:
        settlement_panel = Panel(
            f"[bold green]{hex_obj.settlement.name}[/bold green]\n"
            f"[dim]Velikost: {hex_obj.settlement.size_name}[/dim]\n"
            f"[dim]Vláda: {hex_obj.settlement.government}[/dim]",
            title="🏘️  MYŠÍ OSADA",
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )
        console.print(settlement_panel)
        console.print()

    # Hody
    rolls_text = Text()
    rolls_text.append("🎲 Hody: ", style="dim")
    rolls_text.append(f"Typ k6={hex_obj.type_roll}", style="dim cyan")
    rolls_text.append(f", Kategorie k6={hex_obj.detail_category}", style="dim cyan")
    if hex_obj.detail_subtype:
        rolls_text.append(f", Detail k8={hex_obj.detail_subtype}", style="dim cyan")

    console.print(rolls_text)
    console.print("\n")


@main.group()
def tools():
    """Nástroje pro DM a hráče"""
    pass


@tools.command()
def inventory():
    """
    Správa inventáře

    TODO: Implementovat
    """
    console.print("[yellow]Správa inventáře zatím není implementována[/yellow]")


if __name__ == "__main__":
    main()
