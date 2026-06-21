from dataclasses import dataclass
from typing import List

@dataclass
class CommitInfo:
    author: str
    email: str
    commit_hash: str
    modified_files: List[str]

    def __post_init__(self):
        if not self.author:
            self.author = "<unknown>"
        if not self.email:
            self.email = "<unknown>"