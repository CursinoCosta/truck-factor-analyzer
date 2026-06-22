from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

__all__ = [
    "calculate_truck_factor_commits",
    "CommitsTruckFactorResult",
]

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


def calculate_truck_factor_commits(
    commits: List[CommitInfo],
    coverage_threshold: float = 0.5,
) -> CommitsTruckFactorResult:
    """
    Calcula o Truck Factor baseado em volume de modificações por autor.

    Ordena autores de forma decrescente por contribuição e acumula
    modificações até ultrapassar coverage_threshold do total.
    O número de autores necessários para isso é o Truck Factor.
    """
    if not commits:
        return CommitsTruckFactorResult(
            truck_factor=0,
            critical_authors=[],
            coverage=0.0,
            coverage_threshold=coverage_threshold,
            author_ranking=[],
        )

    totals = _count_modifications(commits)
    grand_total = sum(totals.values())

    if grand_total == 0:
        return CommitsTruckFactorResult(
            truck_factor=0,
            critical_authors=[],
            coverage=0.0,
            coverage_threshold=coverage_threshold,
            author_ranking=list(totals.items()),
        )

    # ordenar de forma decrescente por volume de modificações
    ranking = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    accumulated = 0
    critical_authors: List[str] = []

    for author, count in ranking:
        accumulated += count
        critical_authors.append(author)
        if accumulated / grand_total >= coverage_threshold:
            break

    coverage = accumulated / grand_total

    return CommitsTruckFactorResult(
        truck_factor=len(critical_authors),
        critical_authors=critical_authors,
        coverage=coverage,
        coverage_threshold=coverage_threshold,
        author_ranking=ranking,
    )
