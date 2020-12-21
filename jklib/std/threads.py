"""Utility functions and classes for threads"""


# Built-in
from threading import Thread


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def run_all_threads(threads):
    """
    Runs all the generated threads at once, and then joins them
    :param threads: List of Thread instances we want to run
    :type threads: list(Thread)
    """
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
