"""Utilities to load Git repositories using PyDriller.

This module provides small, testable helpers that extract commit
information from a local git repository using PyDriller.
"""
from dataclasses import dataclass
from typing import List

# PyDriller changed its public API across versions; prefer `Repository` when available.
try:
    from pydriller import Repository  # type: ignore
except Exception:
    from pydriller.repository import Repository  # type: ignore


@dataclass
class CommitInfo:
    author: str
    commit_hash: str
    modified_files: List[str]

    def __post_init__(self):
        if not self.author:
            self.author = "<unknown>"


def load_commits(repo_path: str) -> List[CommitInfo]:
    """Traverse all commits in `repo_path` and return a list of CommitInfo.

    Each CommitInfo contains the author name, commit hash and a list of
    modified file paths (new path if available, otherwise old path).
    """
    commits: List[CommitInfo] = []
    for commit in Repository(repo_path).traverse_commits():
        author = commit.author.name if commit.author and commit.author.name else "<unknown>"
        chash = commit.hash
        files: List[str] = []
        mods = getattr(commit, "modified_files", None) or getattr(commit, "modifications", [])
        for mod in mods:
            # PyDriller's ModifiedFile exposes new_path / old_path
            path = getattr(mod, "new_path", None) or getattr(mod, "old_path", None)
            if path:
                files.append(path)
        commits.append(CommitInfo(author=author, commit_hash=chash, modified_files=files))

    return commits
