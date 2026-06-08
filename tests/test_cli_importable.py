import importlib.util
import pathlib


def test_cli_importable():
    """Ensure `src/cli.py` is importable and exposes `app`."""
    repo_root = pathlib.Path(__file__).parent.parent
    cli_path = repo_root / "src" / "cli.py"
    spec = importlib.util.spec_from_file_location("cli", cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "app")
