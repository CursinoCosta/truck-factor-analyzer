from typing import Optional
import typer

app = typer.Typer(help="Truck Factor Analyzer CLI")


@app.command()
def analyze(repo_path: str = typer.Option(..., "--repo-path", help="Path to the git repository to analyze")) -> None:
    """Analyze a repository (placeholder)."""
    from pathlib import Path

    repo = Path(repo_path)
    if not repo.exists():
        typer.echo(f"Error: path does not exist: {repo_path}")
        raise typer.Exit(code=1)

    try:
        from src.git_loader import load_commits
        from src.metrics import compute_author_stats
    except Exception as exc:
        typer.echo(f"Internal error importing modules: {exc}")
        raise typer.Exit(code=1)

    try:
        commits = load_commits(str(repo))
    except Exception as exc:
        typer.echo(f"Error loading commits: {exc}")
        raise typer.Exit(code=1)

    stats = compute_author_stats(commits)
    if not stats:
        typer.echo("No commits found.")
        return

    typer.echo("Authors:")
    for author, count in sorted(stats.items(), key=lambda x: -x[1]):
        typer.echo(f"{author}: {count} commits")


@app.command()
def info(version: Optional[bool] = typer.Option(False, "--version", "-v", help="Show version")) -> None:
    """Show basic info about the CLI (placeholder)."""
    if version:
        typer.echo("Truck Factor Analyzer 0.1.0")
    else:
        typer.echo("Truck Factor Analyzer — use --version to see version")


if __name__ == "__main__":
    app()
