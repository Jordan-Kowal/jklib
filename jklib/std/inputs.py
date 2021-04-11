"""Utility functions around the "input" mechanic"""

# Built-in
import re


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def choose_from_dict(choices):
    """
    The user must choose a value by inputting the associated key
    :param dict choices: Dict of value/label the user can pick from
    :return: The selected key
    """
    # Displays the initial choices
    input_dict = {x: y for (x, y) in choices.items()}
    input_list = sorted(input_dict.keys())
    input_set = set(input_list)
    messages = [f"{key}: {input_dict[key]}" for key in input_list]
    for message in messages:
        print(message)
    # Answers
    answer = None
    while answer is None:
        answer = input()
        if answer not in input_set:
            answer = None
            print("Invalid input. Your answer must be in the list above.")
    return answer


def input_must_match_regex(regex, error_message):
    """
    The user must type an input that matches a regex. Return his input
    :param regex regex: Regular expression object
    :param str error_message: The error message that must be displayed
    :return: The user's valid answer
    :rtype: str
    """
    answer = None
    while answer is None:
        answer = input()
        if re.search(regex, answer) is None:
            answer = None
            print("Please try again:")
    return answer


def yes_or_no():
    """
    The user must answer with Y or N. Returns a bool
    :return: The answer in boolean format
    :rtype: bool
    """
    answer = None
    while answer is None:
        answer = input().upper()
        if answer == "Y":
            answer = True
        elif answer == "N":
            answer = False
        else:
            answer = None
            print("Invalid input. Your answer must be Y or N")
    return answer
