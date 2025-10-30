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
from src.core.models import Character
from src.generators.character import CharacterGenerator

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
