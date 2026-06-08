import sys
from pathlib import Path

# Ensure the project root (workspace root) is on sys.path so tests can import `src`.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from types import SimpleNamespace

from src.metrics import compute_author_stats


def test_single_author():
    commits = [SimpleNamespace(author="Alice") for _ in range(3)]
    assert compute_author_stats(commits) == {"Alice": 3}


def test_multiple_authors_mixed():
    commits = [
        SimpleNamespace(author="Alice"),
        SimpleNamespace(author=SimpleNamespace(name="Bob")),
        SimpleNamespace(author="Alice"),
        SimpleNamespace(author=None),
        SimpleNamespace(author=SimpleNamespace(name=None)),
        SimpleNamespace(author="Bob"),
    ]
    stats = compute_author_stats(commits)
    assert stats["Alice"] == 2
    assert stats["Bob"] == 2
    assert stats.get("<unknown>", 0) == 2


def test_empty_commits():
    assert compute_author_stats([]) == {}
