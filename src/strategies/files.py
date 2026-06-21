from __future__ import annotations
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List
from src.models import CommitInfo


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