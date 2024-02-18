# Built-in
from typing import List


def clean_text(text: str, olds: List[str], new: str = " ") -> str:
    """Replaces all occurrences of 'olds' with 'new' within a text."""
    for old in olds:
        text = text.replace(old, new)
    text = text.strip()
    return text


def replace_every_nth(text: str, old: str, new: str, nth: int, start: int = 1) -> str:
    """Replaces every nth occurrence of 'old' with 'new' within a text."""
    i = start
    index = text.find(old)
    while index != -1:
        if i == nth:
            text = text[:index] + new + text[index + len(old) :]  # noqa
            i = 0
        index = text.find(old, index + len(old) + 1)
        i += 1
    return text
