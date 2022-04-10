"""Utility functions around the "input" mechanic"""

# Built-in
import re
from typing import Dict


def choose_from_dict(choices: Dict) -> str:
    """The user must choose a value by inputting the associated key"""
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


def input_must_match_regex(regex: str, error_message: str) -> str:
    """The user must type an input that matches a regex. Return his input"""
    answer = None
    while answer is None:
        answer = input()
        if re.search(regex, answer) is None:
            answer = None
            print(f"Please try again: {error_message}")
    return answer


def yes_or_no() -> bool:
    """The user must answer with Y or N. Returns a bool"""
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
