"""
CLI rozhraní pro Mausritter Tools
"""
import click
from rich.console import Console
from rich.table import Table
from src.core.dice import roll, roll_with_details, attribute_test

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
@click.option("--name", "-n", help="Jméno postavy")
def character(name: str):
    """
    Vygeneruj náhodnou postavu

    TODO: Implementovat
    """
    console.print("[yellow]Generátor postav zatím není implementován[/yellow]")
    if name:
        console.print(f"Jméno: {name}")


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
