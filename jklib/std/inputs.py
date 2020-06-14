"""
Contains utility function around the "input" mechanic
Functions:
    choose_from_dict: The user must choose a value by inputting the associated key
    input_must_match_regex: The user must type an input that matches a regex. Return his input
    yes_or_no: The user must answer with Y or N. Returns a bool
"""


# Built-in
import re


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def choose_from_dict(**kwargs):
    """
    The user must choose a value by inputting the associated key
    Args:
        **kwargs (str): param names will be the accepted inputs
    Returns:
        (str) The user input
    """
    # Displays the initial choices
    input_dict = {x: y for (x, y) in kwargs.items()}
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
    Args:
        regex (regex): Regular expression object
        error_message (str): The error message that must be displayed
    Returns:
        (str) The user's valid answer
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
    Returns:
        (bool) The answer in boolean format
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
