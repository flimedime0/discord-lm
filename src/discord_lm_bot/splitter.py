from __future__ import annotations

import re

URL_RE = re.compile(r"https?://\S+")


def split_message(text: str, max_len: int = 2000) -> list[str]:
    """Split ``text`` into Discord-safe segments of length ``max_len``."""
    segments: list[str] = []
    remainder = text
    while len(remainder) > max_len:
        displayed = remainder[:max_len]
        split_at = max_len - 1
        last_url = None
        for m in URL_RE.finditer(displayed, 0, split_at + 1):
            last_url = m
        if last_url and last_url.end() > split_at:
            split_at = max(0, last_url.start() - 1)
        if displayed[split_at].isalnum():
            p_space = displayed.rfind(" ", 0, split_at)
            p_dot = displayed.rfind(".", 0, split_at)
            p = max(p_space, p_dot)
            if p != -1:
                split_at = p
        segment = displayed[: split_at + 1].rstrip()
        remainder = remainder[split_at + 1 :].lstrip()
        if segment:
            segments.append(segment)
    remainder = remainder.strip()
    if remainder:
        segments.append(remainder)
    return segments


__all__ = ["split_message"]
