"""Metrics computation helpers.

Provides small, testable functions to compute metrics from commit data.
"""
from collections import Counter
from typing import Iterable, Dict


def compute_author_stats(commits: Iterable[object]) -> Dict[str, int]:
    """Count commits per author.

    Args:
        commits: An iterable of commit-like objects exposing an `author`
            attribute (string). For compatibility with different commit
            representations, if `author` is not present or falsy the
            author name `"<unknown>"` is used.

    Returns:
        A dict mapping author name to number of commits.
    """
    return dict(
        Counter(
            getattr(
                getattr(c, "author", None),
                "name",
                None
            ) or "<unknown>"
            for c in commits
        )
    )




