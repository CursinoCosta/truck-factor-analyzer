#!/usr/bin/env python3
"""Quick test runner: load commits and print per-author stats.

Usage:
    python test.py /path/to/repo

Run this from the project root so `from src.git_loader` resolves.
"""
import sys
from typing import Iterable


def print_author_stats(commits: Iterable[object]) -> None:
    try:
        from src.metrics import compute_author_stats
    except Exception as exc:
        print("Failed to import compute_author_stats:", exc)
        return

    stats = compute_author_stats(commits)
    if not stats:
        print("No commits found or unable to compute stats.")
        return

    for author, count in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"{author}: {count}")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python test.py /path/to/repo")
        return 2

    repo_path = sys.argv[1]

    try:
        from src.git_loader import load_commits
    except Exception as exc:  # ImportError or other
        print("Failed to import src.git_loader:", exc)
        print("Make sure you run this from the project root and installed requirements (pip install -r requirements.txt).")
        return 1

    try:
        commits = load_commits(repo_path)
    except Exception as exc:
        print("Error while loading commits:", exc)
        return 3

    print_author_stats(commits)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
