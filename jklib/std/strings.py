# coding: utf8
"""
Functions for manipulating and changing string instances and texts
Functions:
    clean_text: Replaces specific characters with a 'replacement' character within a text
    replace_every_nth: Modifies a text by replacing "old" string with "new" string every "nth" time
"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def clean_text(text, char_list, replacement=" "):
    """
    Replaces specific characters with a 'replacement' character within a text
    Args:
        text (str): The text we want to change
        char_list (list): List of strings, which are the subtexts we will replace
        replacement (str, optional): The string used as replacement. Defaults to " ".
    Returns:
        (str) The updated text
    """
    if char_list:
        for char in char_list:
            text = text.replace(char, replacement)
    text = text.strip()
    return text


def replace_every_nth(text, old, new, nth, start=1):
    """
    Modifies a text by replacing "old" string with "new" string every "nth" time
    Args:
        text (str): The text we want to change
        old (str): The string that will be replaced
        new (str): The string used as replacement
        nth (int): The frequency of replacement (every nth occurences)
        start (int, optional): Which occurence to we start with. Defaults to 1.
    Returns:
        (str) The updated text
    """
    i = start
    index = text.find(old)
    while index != -1:
        if i == nth:
            text = text[:index] + new + text[index + len(old) :]
            i = 0
        index = text.find(old, index + len(old) + 1)
        i += 1
    return text
