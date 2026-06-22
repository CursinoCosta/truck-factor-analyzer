from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from src.models import CommitInfo


@dataclass
class CommitsTruckFactorResult:
    truck_factor: int
    critical_authors: List[str]   # autores que juntos ultrapassam o threshold
    coverage: float               # fração real de modificações coberta pelos críticos
    coverage_threshold: float
    author_ranking: List[tuple[str, int]]  # todos os autores ordenados por volume


def _count_modifications(commits: List[CommitInfo]) -> dict[str, int]:
    """
    Soma o número de arquivos modificados por commit para cada autor.
    Cada arquivo em commit.modified_files conta como 1 modificação válida.
    """
    totals: dict[str, int] = {}
    for commit in commits:
        author = commit.author
        count = len(commit.modified_files)
        totals[author] = totals.get(author, 0) + count
    return totals
