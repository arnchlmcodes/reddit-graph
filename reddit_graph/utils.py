"""
Small, stateless helper functions used by the scraper and graph modules.
"""

import math
from datetime import datetime, timezone


def ts(epoch: float) -> str:
    """Convert a UNIX epoch to a ``YYYY-MM-DD`` UTC date string."""
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d")


def clamp(val, lo, hi):
    """Clamp *val* between *lo* and *hi* (inclusive)."""
    return max(lo, min(hi, val))


def score_to_size(score: int, base: int = 10, scale: int = 20, cap: int = 60) -> int:
    """Map a Reddit score to a node pixel-size using a log curve."""
    if score <= 0:
        return base
    return clamp(base + int(math.log1p(score) * scale / math.log1p(100)), base, cap)


def clean(text: str) -> str:
    """Strip non-UTF-8 characters so pyvis internals don't choke."""
    return text.encode("utf-8", errors="replace").decode("utf-8")


def truncate(text: str, n: int = 300) -> str:
    """Return *text* truncated to *n* characters (cleaned first)."""
    text = clean(text)
    return text if len(text) <= n else text[:n] + "..."
