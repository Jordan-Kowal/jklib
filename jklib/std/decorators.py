# Built-in
from time import perf_counter
from typing import Any, Callable


def time_it(function: Callable) -> Callable:
    """Prints the time it takes to run a function."""

    def run_it(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter()
        results = function(*args, **kwargs)
        print(f"{function.__name__} : {perf_counter() - start} seconds")
        return results

    return run_it
