from typing import Optional
import typer

app = typer.Typer(help="Truck Factor Analyzer CLI")


@app.command()
def analyze(repo_path: str = typer.Option(..., "--repo-path", help="Path to the git repository to analyze")) -> None:
    """Analyze a repository (placeholder)."""
    typer.echo(f"Analyzing repository: {repo_path}")


@app.command()
def info(version: Optional[bool] = typer.Option(False, "--version", "-v", help="Show version")) -> None:
    """Show basic info about the CLI (placeholder)."""
    if version:
        typer.echo("Truck Factor Analyzer 0.1.0")
    else:
        typer.echo("Truck Factor Analyzer — use --version to see version")


if __name__ == "__main__":
    app()
