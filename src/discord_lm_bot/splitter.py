import re

URL_RE = re.compile(r"https?://\S+")


def split_message(text: str, max_len: int = 2000) -> list[str]:
    """Split text into URL- and word-safe segments."""
    segments = []
    remaining = text
    while remaining:
        if len(remaining) <= max_len:
            segments.append(remaining.strip())
            break
        split_at = max_len - 1
        last_url = None
        for m in URL_RE.finditer(remaining, 0, split_at + 1):
            last_url = m
        if last_url and last_url.end() > split_at:
            split_at = max(0, last_url.start() - 1)
        if remaining[split_at].isalnum():
            p_space = remaining.rfind(" ", 0, split_at)
            p_dot = remaining.rfind(".", 0, split_at)
            p = max(p_space, p_dot)
            if p != -1:
                split_at = p
        segment = remaining[: split_at + 1]
        segments.append(segment.strip())
        remaining = remaining[split_at + 1 :].lstrip()
    return segments
