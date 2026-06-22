"""Helpers de apresentação visual usando rich."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.strategies.commits import CommitsTruckFactorResult
from src.strategies.files import FileTruckFactorResult

# Console compartilhado por todo o módulo de display.
# stderr=False → saída vai para stdout, compatível com pipes e redirecionamentos.
console = Console(stderr=False)


def _truck_factor_color(tf: int) -> str:
    """Cor semântica baseada no valor do Truck Factor."""
    if tf <= 1:
        return "bold red"
    if tf <= 3:
        return "bold yellow"
    return "bold green"


def render_result_panel(
    result: CommitsTruckFactorResult | FileTruckFactorResult,
    strategy: str,
) -> None:
    """Exibe painel com o valor do Truck Factor e a cobertura alcançada."""
    tf = result.truck_factor
    color = _truck_factor_color(tf)

    coverage_pct = round(
        result.coverage * 100
        if hasattr(result, "coverage")
        else result.coverage_before * 100,
        1,
    )

    body = Text()
    body.append(f"  Truck Factor: ", style="bold white")
    body.append(f"{tf}\n", style=color)
    body.append(f"  Strategy:     ", style="bold white")
    body.append(f"{strategy}\n", style="cyan")
    body.append(f"  Coverage:     ", style="bold white")
    body.append(f"{coverage_pct}%", style="white")

    console.print(
        Panel(body, title="[bold]Truck Factor Analyzer[/bold]", expand=False)
    )


def render_authors_table(
    result: CommitsTruckFactorResult | FileTruckFactorResult,
) -> None:
    """Exibe tabela com os autores críticos e seus volumes de contribuição."""
    table = Table(title="Autores críticos", show_lines=False, expand=False)
    table.add_column("#",       style="dim",        width=4)
    table.add_column("Autor",   style="bold white",  min_width=20)
    table.add_column("Volume",  style="cyan",        justify="right")
    table.add_column("Status",  justify="center")

    critical_set = set(result.critical_authors)

    # CommitsTruckFactorResult tem author_ranking; FileTruckFactorResult não
    if hasattr(result, "author_ranking"):
        ranking = result.author_ranking
    else:
        ranking = [(a, "—") for a in result.critical_authors]

    for i, (author, volume) in enumerate(ranking, start=1):
        is_critical = author in critical_set
        status = "[bold red]⚠ crítico[/bold red]" if is_critical else "[green]ok[/green]"
        table.add_row(str(i), author, str(volume), status)

    console.print(table)
