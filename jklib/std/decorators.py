"""Generic decorators for various uses"""


# Built-in
from time import perf_counter


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def time_it(function):
    """Times a function and prints its runtime in the console"""

    def run_it(*args, **kwargs):
        time_before = perf_counter()
        results = function(*args, **kwargs)
        time_total = perf_counter() - time_before
        print(f"{function.__name__} : {time_total} seconds")
        return results

    return run_it
