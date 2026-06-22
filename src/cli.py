from pathlib import Path

import typer

from src.git_loader import load_commits

app = typer.Typer(help="Truck Factor Analyzer CLI")


@app.command()
def analyze(
    repo_path: str = typer.Option(..., "--repo-path", help="Path to the git repository to analyze"),
    strategy: str = typer.Option("commits", "--strategy", help="Estimation strategy: 'commits' or 'files'"),
) -> None:
    """Analyze a git repository and compute its Truck Factor."""

    repo = Path(repo_path)

    if not repo.exists():
        typer.echo(f"Error: path does not exist: {repo_path}")
        raise typer.Exit(code=1)

    try:
        commits = load_commits(str(repo))
    except Exception as exc:
        typer.echo(f"Error loading repository: {exc}")
        raise typer.Exit(code=1)

    if not commits:
        typer.echo("No commits found.")
        return

    if strategy == "commits":
        from src.strategies.commits import calculate_truck_factor_commits
        result = calculate_truck_factor_commits(commits)
    elif strategy == "files":
        from src.strategies.files import calculate_truck_factor_files
        result = calculate_truck_factor_files(commits)
    else:
        valid = ("commits", "files")
        typer.echo(
            f"Error: '{strategy}' is not a valid strategy.\n"
            f"Available strategies: {', '.join(valid)}\n"
            f"Example: --strategy commits"
        )
        raise typer.Exit(code=1)

    from src.display import render_result_panel, render_authors_table
    render_result_panel(result, strategy)
    render_authors_table(result)


@app.command()
def version() -> None:
    """Show CLI version."""
    typer.echo("Truck Factor Analyzer 0.1.0")


if __name__ == "__main__":
    app()
