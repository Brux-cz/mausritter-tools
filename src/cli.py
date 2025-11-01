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
from src.core.models import Character, NPC, Hireling, Weather
from src.generators.character import CharacterGenerator
from src.generators.npc import NPCGenerator
from src.generators.hireling import HirelingGenerator
from src.generators.weather import WeatherGenerator

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
