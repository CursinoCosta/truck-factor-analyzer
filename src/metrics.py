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
    names = []
    for c in commits:
        name = getattr(c, "author", None)
        # If author is an object with a `name` attribute (e.g. PyDriller Developer)
        if name and not isinstance(name, str):
            name = getattr(name, "name", None)
        if not name:
            name = "<unknown>"
        names.append(name)

    return dict(Counter(names))

