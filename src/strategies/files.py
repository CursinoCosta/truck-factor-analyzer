from __future__ import annotations
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List
from src.models import CommitInfo

__all__ = [
    "calculate_truck_factor_files",
    "FileTruckFactorResult",
    "FileAuthorshipTracker",
    "PRIMARY_AUTHOR_THRESHOLD",
]
    
PRIMARY_AUTHOR_THRESHOLD = 0.75


@dataclass
class FileAuthorshipTracker:
    """Acumula as variáveis FA, DL e AC por arquivo e autor."""

    # FA: autor que fez o primeiro commit tocando esse arquivo
    fa: dict[str, str] = field(default_factory=dict)

    # DL: número de edições diretas do autor nesse arquivo
    dl: DefaultDict[tuple[str, str], int] = field(
        default_factory=lambda: defaultdict(int)
    )

    # AC: edições feitas por terceiros nesse arquivo
    ac: DefaultDict[tuple[str, str], int] = field(
        default_factory=lambda: defaultdict(int)
    )

    def process_commits(self, commits: List[CommitInfo]) -> None:
            """Itera cronologicamente sobre commits e registra FA, DL e AC."""
            for commit in commits:
                author = commit.author
                for filepath in commit.modified_files:
                    # FA: o primeiro autor que tocou o arquivo é o first author
                    if filepath not in self.fa:
                        self.fa[filepath] = author

                    # DL: toda edição desse autor nesse arquivo conta
                    self.dl[(filepath, author)] += 1

                    # AC: se quem edita NÃO é o first author, incrementa AC do first author
                    first_author = self.fa[filepath]
                    if author != first_author:
                        self.ac[(filepath, first_author)] += 1

def _compute_doa(fa: int, dl: int, ac: int) -> float:
    """
    DOA = 3.293 + 1.098*FA + 0.164*DL - 0.321*ln(1 + AC)

    fa: 1 se o dev é first author do arquivo, 0 caso contrário
    dl: número de edições diretas do dev no arquivo
    ac: número de edições de terceiros no arquivo (perspectiva do dev)

    max(ac, 0) evita log de negativo; (1 + ac) evita log(0).
    """
    return 3.293 + 1.098 * fa + 0.164 * dl - 0.321 * math.log(1 + max(ac, 0))

def _normalize_doa_per_file(
    raw_scores: dict[tuple[str, str], float],
) -> dict[tuple[str, str], float]:
    """
    Por arquivo, divide todos os scores pelo score máximo.
    O autor com maior DOA recebe 1.0; os demais ficam entre 0 e 1.
    """
    by_file: DefaultDict[str, list[tuple[str, float]]] = defaultdict(list)
    for (filepath, author), score in raw_scores.items():
        by_file[filepath].append((author, score))

    normalized: dict[tuple[str, str], float] = {}
    for filepath, entries in by_file.items():
        max_score = max(s for _, s in entries)
        for author, score in entries:
            normalized[(filepath, author)] = (score / max_score) if max_score > 0 else 0.0
    return normalized

def _build_authorship_map(
    tracker: FileAuthorshipTracker,
    threshold: float = PRIMARY_AUTHOR_THRESHOLD,
) -> dict[str, set[str]]:
    """
    Retorna {filepath -> conjunto de autores primários}.
    Um autor é primário se seu DOA normalizado >= threshold.
    """
    all_files = set(tracker.fa.keys())
    # todos os autores que aparecem como first author ou fizeram ao menos 1 DL
    all_authors: set[str] = set(tracker.fa.values()) | {
        author for (_, author) in tracker.dl.keys()
    }

    raw: dict[tuple[str, str], float] = {}
    for filepath in all_files:
        first_author = tracker.fa[filepath]
        for author in all_authors:
            dl_val = tracker.dl[(filepath, author)]
            ac_val = tracker.ac[(filepath, author)]
            fa_val = 1 if author == first_author else 0
            # só calcula DOA se o autor tem alguma relação com o arquivo
            if dl_val > 0 or fa_val == 1:
                raw[(filepath, author)] = _compute_doa(fa_val, dl_val, ac_val)

    normalized = _normalize_doa_per_file(raw)

    authorship_map: dict[str, set[str]] = {f: set() for f in all_files}
    for (filepath, author), norm_score in normalized.items():
        if norm_score >= threshold:
            authorship_map[filepath].add(author)

    return authorship_map

def _compute_coverage(
    active_authors: set[str],
    authorship_map: dict[str, set[str]],
) -> float:
    """
    Fração de arquivos que possuem ao menos um autor primário
    dentro do conjunto active_authors. Retorna 0.0 se sem arquivos.
    """
    total = len(authorship_map)
    if total == 0:
        return 0.0
    covered = sum(
        1 for owners in authorship_map.values()
        if owners & active_authors 
    )
    return covered / total

@dataclass
class FileTruckFactorResult:
    truck_factor: int
    critical_authors: List[str]  # autores removidos até atingir o limite
    coverage_before: float       # cobertura com equipe completa
    coverage_threshold: float


def calculate_truck_factor_files(
    commits: List[CommitInfo],
    coverage_threshold: float = 0.5,
) -> FileTruckFactorResult:
    """
    Calcula o Truck Factor pela heurística DOA

    Remove iterativamente o autor com mais arquivos únicos sob sua autoria
    enquanto a cobertura restante ainda >= coverage_threshold.
    O número de remoções é o Truck Factor.
    """
    tracker = FileAuthorshipTracker()
    tracker.process_commits(commits)
    authorship_map = _build_authorship_map(tracker)

    active_authors: set[str] = set(tracker.fa.values()) | {
        a for (_, a) in tracker.dl.keys()
    }
    coverage_before = _compute_coverage(active_authors, authorship_map)

    truck_factor = 0
    critical_authors: List[str] = []

    while active_authors:
        if _compute_coverage(active_authors, authorship_map) < coverage_threshold:
            break

        def unique_files(author: str) -> int:
            return sum(
                1 for owners in authorship_map.values()
                if owners == {author}
            )

        candidate = max(active_authors, key=unique_files)
        remaining = active_authors - {candidate}

        if _compute_coverage(remaining, authorship_map) < coverage_threshold:
            break

        active_authors = remaining
        critical_authors.append(candidate)
        truck_factor += 1

    return FileTruckFactorResult(
        truck_factor=truck_factor,
        critical_authors=critical_authors,
        coverage_before=coverage_before,
        coverage_threshold=coverage_threshold,
    )