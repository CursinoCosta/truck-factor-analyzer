#!/usr/bin/env python3
"""Quick test runner for `src.git_loader.load_commits`.

Usage:
    python test.py /path/to/repo

Run this from the project root so `from src.git_loader` resolves.
"""
import sys


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

    for c in commits:
        print(f"{c.commit_hash} | {c.author} | {len(c.modified_files)} files")
        for f in c.modified_files:
            print("  ", f)

    print(f"Total commits: {len(commits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
