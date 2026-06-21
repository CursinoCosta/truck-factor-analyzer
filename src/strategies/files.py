from __future__ import annotations
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