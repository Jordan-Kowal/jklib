"""Classes and functions to perform actions in Django commands."""

# Built-in
from typing import List, Optional, Type

# Third-party
from colorama import Fore
from colorama import init as colorama_init


class Color:
    """Class to define the color used in Operation and Task printed
    messages."""

    # Hierarchy
    operation = Fore.WHITE
    task = Fore.CYAN
    reset = Fore.RESET

    # Workflow
    success = Fore.GREEN
    info = Fore.MAGENTA
    warning = Fore.YELLOW
    error = Fore.RED


class Operation:
    """List of instructions to be run within a Django commands.

    Made of several Task instances. To be used with our
    `ImprovedCommand` custom class
    """

    name: Optional[str] = None
    tasks: List[Type["Task"]] = []

    # ----------------------------------------
    # Workflow
    # ----------------------------------------
    def run(self) -> None:
        """Main method.

        Performs all tasks one by one and prints feedback
        """
        colorama_init()
        self.print_operation_start()
        operation_success = self.run_tasks()
        if operation_success:
            self.print_operation_success()
        else:
            self.print_operation_fail()

    def run_tasks(self) -> bool:
        """Runs all the operation tasks."""
        success = True
        task_instances = [task() for task in self.tasks]
        for i, task_instance in enumerate(task_instances):
            self.print_task_start(task_instance, i)
            try:
                task_instance.run()
            except Exception as e:
                task_instance.print_error(f"{e}")
                self.print_task_fail(task_instance)
                success = False
                break
            else:
                self.print_task_success(task_instance)
                continue
        return success

    @property
    def total_tasks(self) -> int:
        """Task quantity in our Operation."""
        return len(self.tasks)

    # ----------------------------------------
    # Feedback (in chronological order)
    # ----------------------------------------
    def print_operation_start(self) -> None:
        """Prints a message to indicate the start of the operation."""
        print(f"{Color.operation}Starting operation '{self.name}' ...{Color.reset}\n")

    def print_task_start(self, task: "Task", number: int) -> None:
        """Prints a message to indicate which task (name and number) is
        starting."""
        wrapper = "~" * 50
        wrapper = f"{Color.operation}{wrapper}{Color.reset}"
        print(wrapper)
        print(
            f"{Color.operation}~~~~~ Task {Color.task}{number+1}{Color.operation}/{self.total_tasks}: "
            + f"{Color.task}{task.name}{Color.reset}"
        )
        print(wrapper)

    @staticmethod
    def print_task_fail(task: "Task") -> None:
        """Prints an error message indicating the task has failed."""
        print(
            f"{Color.error}Task '{Color.task}{task.name}{Color.error}' has failed{Color.reset}\n"
        )

    @staticmethod
    def print_task_success(task: "Task") -> None:
        """Prints a message indicating the task was a success."""
        print(
            f"{Color.success}Task '{Color.task}{task.name}{Color.success}' has ended successfully{Color.reset}\n"
        )

    def print_operation_fail(self) -> None:
        """Prints an error message indicating the Operation one task failed."""
        print(
            f"{Color.error}Operation '{self.name}' could not be run entirely.{Color.reset}"
        )
        print(f"{Color.error}Please check the logs above.{Color.reset}")

    def print_operation_success(self) -> None:
        """Prints a success message indicating that all tasks were run
        successfully."""
        print(f"{Color.success}Operation '{self.name}' was a success.{Color.reset}")


class Task:
    """Individual task/step during an Operation.

    Used to split up the logic
    """

    name: Optional[str] = None
    message_suffix: str = "--->"

    def run(self) -> None:
        """Main function.

        Must execute the process/task logic
        """
        raise NotImplementedError()

    # ----------------------------------------
    # Feedback
    # ----------------------------------------
    def print_error(self, message: str) -> None:
        """Prints a colored error message."""
        self._print_message(message, "error", Color.error)

    def print_info(self, message: str) -> None:
        """Prints a colored info message."""
        self._print_message(message, "info", Color.info)

    def print_success(self, message: str) -> None:
        """Prints a colored success message."""
        self._print_message(message, "success", Color.success)

    def print_warning(self, message: str) -> None:
        """Prints a colored warning message."""
        self._print_message(message, "warning", Color.warning)

    def _print_message(self, message: str, type_: str, color: Color) -> None:
        """Prints a message in the right color and prefix it with a type."""
        print(f"{color}{self.message_suffix} [{type_.upper()}] {message}{Color.reset}")
