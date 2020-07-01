"""Utility functions for working with strings"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def clean_text(text, char_list, replacement=" "):
    """
    Replaces specific characters with a 'replacement' character within a text
    :param str text:  The text we want to change
    :param char_list: List of strings, which are the subtexts we will replace
    :type char_list: list(str)
    :param str replacement: The string used as replacement. Defaults to " ".
    :return: The updated string
    :rtype: str
    """
    if char_list:
        for char in char_list:
            text = text.replace(char, replacement)
    text = text.strip()
    return text


def replace_every_nth(text, old, new, nth, start=1):
    """
    Modifies a text by replacing "old" string with "new" string every "nth" time
    :param str text: The text we want to change
    :param str old: The string that will be replaced
    :param str new: The string used as replacement
    :param int nth: The frequency of replacement (every nth occurrences)
    :param int start: Which occurrence to we start with. Defaults to 1.
    :return: The updated text
    :rtype: str
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
