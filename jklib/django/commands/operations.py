"""Classes and functions to perform actions in Django commands"""

# Third-party
from colorama import Fore
from colorama import init as colorama_init


# --------------------------------------------------------------------------------
# > Helpers
# --------------------------------------------------------------------------------
class Color:
    """Class to define the color used in Operation and Task printed messages"""

    # Hierarchy
    operation = Fore.WHITE
    task = Fore.CYAN
    reset = Fore.RESET

    # Workflow
    success = Fore.GREEN
    info = Fore.MAGENTA
    warning = Fore.YELLOW
    error = Fore.RED


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class Operation:
    """
    List of instructions to be run within a Django commands. Made of several Task instances.
    To be used with our `ImprovedCommand` custom class
    """

    name = None
    tasks = []

    # ----------------------------------------
    # Workflow
    # ----------------------------------------
    def run(self):
        """Main method. Performs all tasks one by one and prints feedback"""
        colorama_init()
        self.print_operation_start()
        operation_success = self.run_tasks()
        if operation_success:
            self.print_operation_success()
        else:
            self.print_operation_fail()

    def run_tasks(self):
        """Runs all the operation tasks"""
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
        """Prints a message to indicate the start of the operation"""
        print(f"{Color.operation}Starting operation '{self.name}' ...{Color.reset}\n")

    def print_task_start(self, task, number):
        """
        Prints a message to indicate which task (name and number) is starting
        :param Task task: The task instance we're running
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
        :param Task task: The task instance that failed
        """
        print(
            f"{Color.error}Task '{Color.task}{task.name}{Color.error}' has failed{Color.reset}\n"
        )

    @staticmethod
    def print_task_success(task):
        """
        Prints a message indicating the task was a success
        :param Task task: The task instance that was a success
        """
        print(
            f"{Color.success}Task '{Color.task}{task.name}{Color.success}' has ended successfully{Color.reset}\n"
        )

    def print_operation_fail(self):
        """Prints an error message indicating the Operation one task failed"""
        print(
            f"{Color.error}Operation '{self.name}' could not be run entirely.{Color.reset}"
        )
        print(f"{Color.error}Please check the logs above.{Color.reset}")

    def print_operation_success(self):
        """Prints a success message indicating that all tasks were run successfully"""
        print(f"{Color.success}Operation '{self.name}' was a success.{Color.reset}")


class Task:
    """Individual task/step during an Operation. Used to split up the logic"""

    name = None
    message_suffix = "--->"

    # ----------------------------------------
    # Workflow
    # ----------------------------------------
    def run(self):
        """Main function. Must execute the process/task logic"""
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
        Prints a message in the right color and prefix it with a type
        :param str message: The message to show in the console
        :param str type_: The type of message
        :param color: The color to apply to the whole thing
        """
        print(f"{color}{self.message_suffix} [{type_.upper()}] {message}{Color.reset}")
