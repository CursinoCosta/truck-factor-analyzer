from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict


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