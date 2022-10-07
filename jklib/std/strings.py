"""Utility functions for working with strings."""
# Built-in
from typing import List


def clean_text(text: str, char_list: List[str], replacement: str = " ") -> str:
    """Replaces specific characters with a 'replacement' character within a
    text."""
    if char_list:
        for char in char_list:
            text = text.replace(char, replacement)
    text = text.strip()
    return text


def replace_every_nth(text: str, old: str, new: str, nth: int, start: int = 1) -> str:
    """Modifies a text by replacing "old" string with "new" string every "nth"
    time."""
    i = start
    index = text.find(old)
    while index != -1:
        if i == nth:
            text = text[:index] + new + text[index + len(old) :]
            i = 0
        index = text.find(old, index + len(old) + 1)
        i += 1
    return text
