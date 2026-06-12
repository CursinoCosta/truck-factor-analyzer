from typing import Optional
from pathlib import Path
import typer

from src.git_loader import load_commits
from src.metrics import compute_author_stats, sort_author_stats

app = typer.Typer(help="Truck Factor Analyzer CLI")


@app.command()
def analyze(
    repo_path: str = typer.Option(..., "--repo-path", help="Path to the git repository to analyze")
) -> None:
    """Analyze a git repository and show author contribution stats."""

    repo = Path(repo_path)

    if not repo.exists():
        typer.echo(f"Error: path does not exist: {repo_path}")
        raise typer.Exit(code=1)

    try:
        commits = load_commits(str(repo))
    except Exception as exc:
        typer.echo(f"Error loading repository: {exc}")
        raise typer.Exit(code=1)

    stats = compute_author_stats(commits)

    if not stats:
        typer.echo("No commits found.")
        return

    sorted_stats = sort_author_stats(stats)

    typer.echo("Authors:")
    for author, count in sorted_stats:
        typer.echo(f"{author}: {count} commits")


@app.command()
def version() -> None:
    """Show CLI version."""
    typer.echo("Truck Factor Analyzer 0.1.0")


if __name__ == "__main__":
    app()