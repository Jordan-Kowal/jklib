"""Classes and functions for Django commands"""


# Django
from django.core.management.base import BaseCommand


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ImprovedCommand(BaseCommand):
    """Extends BaseCommand to work with Operation instances"""

    operation_class = None

    def run_operation(self, *args):
        """Instantiate the operation with the args and runs it"""
        operation = self.operation_class(*args)
        operation.run()

    @staticmethod
    def ask_user_to_proceed():
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
