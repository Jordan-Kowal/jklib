"""Utility functions and classes for threads."""
# Built-in
from threading import Thread
from typing import List


def run_all_threads(threads: List[Thread]) -> None:
    """Runs all the generated threads at once, and then joins them."""
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
