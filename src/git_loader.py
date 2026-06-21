"""Utilities to load Git repositories using PyDriller.

This module provides small, testable helpers that extract commit
information from a local git repository using PyDriller.
"""
from typing import List
from pathlib import Path

# Tente importar o Repository (PyDriller mudou a API ao longo das versões)
try:
    from pydriller import Repository  # type: ignore
except Exception:
    from pydriller.repository import Repository  # type: ignore

from src.models import CommitInfo
from src.aliases import unificar_autores

# Conjuntos de exclusão
IGNORED_EXTENSIONS = {
    ".md", ".txt", ".json", ".xml", ".yml", ".yaml", ".csv", 
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".lock"
}

IGNORED_DIRECTORIES = {
    "node_modules", "vendor", "venv", ".venv", "env", 
    "dist", "build", "target", "out", "site-packages"
}

def ignorar_arquivo(file_path: str) -> bool:
    """Verifica se um arquivo deve ser ignorado na análise."""
    path = Path(file_path)
    
    # Verifica a extensão
    if path.suffix.lower() in IGNORED_EXTENSIONS:
        return True
        
    # Verifica se alguma das pastas no caminho está na lista de ignoradas
    if any(part in IGNORED_DIRECTORIES for part in path.parts):
        return True
        
    return False


def load_commits(repo_path: str) -> List[CommitInfo]:
    """Traverse all commits in `repo_path` and return a list of CommitInfo.

    Each CommitInfo contains the author name, commit hash and a list of
    modified file paths (new path if available, otherwise old path).
    """
    commits: List[CommitInfo] = []
    for commit in Repository(repo_path).traverse_commits():
        author = commit.author.name if commit.author and commit.author.name else "<unknown>"
        email = commit.author.email if commit.author and commit.author.email else "<unknown>"
        chash = commit.hash
        files: List[str] = []
        mods = getattr(commit, "modified_files", None) or getattr(commit, "modifications", [])
        for mod in mods:
            # PyDriller's ModifiedFile exposes new_path / old_path
            path = getattr(mod, "new_path", None) or getattr(mod, "old_path", None)
            if path and not ignorar_arquivo(path):
                files.append(path)
        if files:
            commits.append(CommitInfo(author=author, email=email, commit_hash=chash, modified_files=files))

    commits_limpos = unificar_autores(commits)
    return commits_limpos
