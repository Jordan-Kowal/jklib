"""
Classes and functions for handling actions of a Django command
Contains 2 classes for running and providing feedback during Django commands
    Operation           Called in a Django command. Runs all given tasks until one fails
    OperationTask       Individual task/action performed during an operation

The way it works is:
    You create a new Command
    It calls an Operation
    This Operation is made of several OperationTask classes
    Each OperationTask perform a specific part of the operation
"""


# Third-party
from colorama import Fore
from colorama import init as colorama_init


# --------------------------------------------------------------------------------
# > Helpers
# --------------------------------------------------------------------------------
class Color:
    """Class to define the color used in Operation and OperationTask printed messages"""

    # Hierarchy
    operation = Fore.MAGENTA
    task = Fore.CYAN
    reset = Fore.RESET

    # Workflow
    success = Fore.GREEN
    info = Fore.WHITE
    warning = Fore.YELLOW
    error = Fore.RED


# --------------------------------------------------------------------------------
# > Main Classes
# --------------------------------------------------------------------------------
class Operation:
    """
    A list of OperationTask that should contain the entire workflow of a Django Command
    This class should be called within the 'handle' method of a Django Command class
    To run your Operation, simply call the .run() method
    """

    name = None
    tasks = []

    # ----------------------------------------
    # Workflow
    # ----------------------------------------
    def run(self):
        """
        Main function to call when you want to execute/perform your actions
        It will run all its task one by one until all are done or one failed
        Provides feedback in the console/shell
        """
        colorama_init()
        self.print_operation_start()
        operation_success = self.run_tasks()
        if operation_success:
            self.print_operation_success()
        else:
            self.print_operation_fail()

    def run_tasks(self):
        """
        Runs all tasks in order, until all are done and one fails
        Feedback will depends on task content and their results
        """
        success = True
        task_instances = [task() for task in self.tasks]
        for i, task_instance in enumerate(task_instances):
            self.print_task_start(task_instance, i)
            try:
                task_instance.run()
            except Exception as e:
                task_instance.print_error(e)
                self.print_task_fail(task_instance)
                success = False
                break
            else:
                self.print_task_success(task_instance)
                continue
        return success

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    @property
    def total_tasks(self):
        """
        :return: The number of tasks in this Operation
        :rtype: int
        """
        return len(self.tasks)

    # ----------------------------------------
    # Feedback (in chronological order)
    # ----------------------------------------
    def print_operation_start(self):
        """Prints a message to indicate the start of the process"""
        print(f"{Color.operation}Starting operation '{self.name}' ...{Color.reset}\n")

    def print_task_start(self, task, number):
        """
        Prints a message to indicate which task (name and number) is starting
        :param OperationTask task: The task instance we're running
        :param int number: The number of the current task
        """
        wrapper = "~" * 50
        wrapper = f"{Color.operation}{wrapper}{Color.reset}"
        print(wrapper)
        print(
            f"{Color.operation}~~~~~ Task {Color.task}{number+1}{Color.operation}/{self.total_tasks}: "
            + f"{Color.task}{task.name}{Color.reset}"
        )
        print(wrapper)

    @staticmethod
    def print_task_fail(task):
        """
        Prints an error message indicating the task has failed
        :param OperationTask task: The task instance that failed
        """
        print(
            f"{Color.error}Task '{Color.task}{task.name}{Color.error}' has failed{Color.reset}\n"
        )

    @staticmethod
    def print_task_success(task):
        """
        Prints a message indicating the task was a success
        :param OperationTask task: The task instance that was a success
        """
        print(
            f"{Color.success}Task '{Color.task}{task.name}{Color.success}' has ended successfully{Color.reset}\n"
        )

    def print_operation_fail(self):
        """Prints an error message indicating the Operation one task failed"""
        print(
            f"{Color.error}Operation '{self.name}' could not be run entirely.{Color.reset}"
        )
        print(f"{Color.error}Please check the log above.{Color.reset}\n")

    def print_operation_success(self):
        """Prints a success message indicating that all tasks were run successfully"""
        print(f"{Color.error}Operation '{self.name}' was a success.{Color.reset}\n")


class OperationTask:
    """
    Individual task that will be performed during an Operation
    Used to better split/segment Operation actions
    To use, you must:
        Implement your main logic in the "run" method
        Provide a "name" attribute
    """

    name = None
    message_suffix = "--->"

    # ----------------------------------------
    # Workflow
    # ----------------------------------------
    def run(self):
        """
        Main function that will be called during an Operation. Must be overridden
        Should return a boolean (indicating success or failure)
        """
        raise NotImplementedError()

    # ----------------------------------------
    # Feedback
    # ----------------------------------------
    def print_error(self, message):
        """
        Prints a colored error message
        :param str message: The message shown in the console
        """
        self._print_message(message, "error", Color.error)

    def print_info(self, message):
        """
        Prints a colored info message
        :param str message: The message shown in the console
        """
        self._print_message(message, "info", Color.info)

    def print_success(self, message):
        """
        Prints a colored success message
        :param str message: The message shown in the console
        """
        self._print_message(message, "success", Color.success)

    def print_warning(self, message):
        """
        Prints a colored warning message
        :param str message: The message shown in the console
        """
        self._print_message(message, "warning", Color.warning)

    def _print_message(self, message, type_, color):
        """
        Shared printing function that prepends:
            Changes the color of the message
            Prepends a string to make it more readable
            Adds a message type in between brackets
            Shows the message
            And reset the color back to normal
        :param str message: The message to show in the console
        :param str type_: The type of message
        :param color: The color to apply to the whole thing
        """
        print(f"{color}{self.message_suffix} [{type_.upper()}] {message}{Color.reset}")
