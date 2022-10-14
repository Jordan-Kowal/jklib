"""Classes and functions for Django commands."""


# Built-in
from typing import Any, Optional, Type

# Django
from django.core.management.base import BaseCommand

# Local
from .operations import Operation


class ImprovedCommand(BaseCommand):
    """Extends BaseCommand to work with Operation instances."""

    operation_class: Optional[Type[Operation]] = None

    def run_operation(self, *args: Any) -> None:
        """Instantiate the operation with the args and runs it."""
        if self.operation_class is not None:
            operation: Operation = self.operation_class(*args)
            operation.run()

    @staticmethod
    def ask_user_to_proceed() -> bool:
        """
        Ask the user if he wants to proceed and returns a boolean answer
        :return: Whether to proceed
        :rtype: bool
        """
        print("Do you wish to proceed ? (y/n)")
        proceed = None
        while proceed is None:
            answer = input("").lower()
            if answer == "y":
                proceed = True
            elif answer == "n":
                print("Aborting operation...")
                proceed = False
            else:
                print("Invalid answer. Please type 'y' for yes or 'n' for no")
        return proceed
