"""Custom test runners."""

# Built-in
import re
from time import perf_counter
from typing import Dict, List, Optional
from unittest import TestResult, TextTestResult, TextTestRunner

# Django
from django.test import runner

# Terminal Colors
ERROR_COLOR = "\033[91m"
SUCCESS_COLOR = "\033[92m"
FAILURE_COLOR = "\033[93m"
ENDC_COLOR = "\033[0m"


class Result:
    """Represents a test result with its name, result, and execution time."""

    DEFAULT_SYMBOL = "?"
    SUCCESS_SYMBOL = "."
    ERROR_SYMBOL = "E"
    FAILURE_SYMBOL = "F"

    def __init__(self, test) -> None:
        #       test_name            app                                   case
        #  |------------------|  |--------|                   |----------------------------|
        # "test_unique_together (receptions.tests.test_models.ReceptionStatusHistoryTestCase)"
        self.test = test
        match = re.match("^(.+) \((.+)\)$", str(test))  # noqa: W605
        self.app: str = match.group(2).split(".")[0]
        self.case: str = match.group(2).split(".")[-1]
        self.test_name: str = match.group(1)
        self.start: float = perf_counter()
        self.end: Optional[float] = None
        self.symbol: str = self.DEFAULT_SYMBOL

    def __str__(self) -> str:
        return f"{self.test}"

    @property
    def duration(self) -> float:
        if self.end is None:
            return 0.0
        return round(self.end - self.start, 6)

    @property
    def color(self) -> str:
        if self.symbol == self.SUCCESS_SYMBOL:
            return SUCCESS_COLOR
        if self.symbol == self.ERROR_SYMBOL:
            return ERROR_COLOR
        if self.symbol == self.FAILURE_SYMBOL:
            return FAILURE_COLOR
        return ENDC_COLOR

    def set_error(self) -> None:
        self.symbol = self.ERROR_SYMBOL
        self.end = perf_counter()

    def set_failure(self) -> None:
        self.symbol = self.FAILURE_SYMBOL
        self.end = perf_counter()

    def set_success(self) -> None:
        self.symbol = self.SUCCESS_SYMBOL
        self.end = perf_counter()


class TimedTextTestResult(TextTestResult):
    """Extends TextTestResult to track execution time of each test and print
    them."""

    def __init__(self, *args, **kwargs) -> None:
        super(TimedTextTestResult, self).__init__(*args, **kwargs)
        self.clocks: Dict[str, Result] = dict()
        self.unknown_errors: List[Result] = []

    def startTest(self, test) -> None:
        self.clocks[f"{test}"] = Result(test)
        super().startTest(test)

    def addError(self, test, err) -> None:
        result = self._get_result(test)
        result.set_error()
        super().addError(test, err)

    def addFailure(self, test, err) -> None:
        result = self._get_result(test)
        result.set_failure()
        super().addFailure(test, err)

    def addSuccess(self, test) -> None:
        result = self._get_result(test)
        result.set_success()
        super().addSuccess(test)

    def show_execution_times(self) -> None:
        results = self.clocks.values()
        max_app_length = max([len(r.app) for r in results]) + 2
        max_case_length = max([len(r.case) for r in results]) + 2
        max_test_name_length = max([len(r.test_name) for r in results]) + 2
        print(
            f"\n{'APP'.ljust(max_app_length)}"
            f"{'CASE'.ljust(max_case_length)}"
            f"{'TEST_NAME'.ljust(max_test_name_length)}"
            f"   TIME"
        )
        for result in self.clocks.values():
            print(
                f"{result.color}"
                f"{result.app.ljust(max_app_length)}"
                f"{result.case.ljust(max_case_length)}"
                f"{result.test_name.ljust(max_test_name_length)}"
                f"{result.symbol.ljust(3)}"
                f"{result.duration}s"
                f"{ENDC_COLOR}"
            )

    def show_unknown_errors(self) -> None:
        if len(self.unknown_errors) == 0:
            return
        print(
            f"\n{ERROR_COLOR}"
            f"The test run also encountered some unexpected issues in:"
            f"{ENDC_COLOR}"
        )
        for result in self.unknown_errors:
            print(f"\t{FAILURE_COLOR}{result.test}{ENDC_COLOR}")

    def _get_result(self, test) -> Result:
        """We might end up with an unknown key when crashing in a setUpClass
        method All its tests will be ignored, but to avoid crashing, we create
        a test result on the fly And store that result in the unknown errors
        list."""
        result = self.clocks.get(f"{test}")
        if result is None:
            result = Result(test)
            self.unknown_errors.append(result)
        return result


class TimedTextTestRunner(TextTestRunner):
    """Extend TextTestRunner to show the execution times at the end."""

    resultclass = TimedTextTestResult

    def run(self, test) -> TestResult:
        result = super().run(test)
        result.show_execution_times()
        result.show_unknown_errors()
        print()
        return result


class CustomTestRunner(runner.DiscoverRunner):
    """Custom runner that simply tracks and prints the test execution times."""

    test_runner = TimedTextTestRunner
