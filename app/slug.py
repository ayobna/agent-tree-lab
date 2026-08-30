import re


def slugify(title: str) -> str:
    """Turn a human title into a URL-safe slug."""
    s = title.strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")