from threading import Thread
from typing import List


def run_all_threads(threads: List[Thread]) -> None:
    """Runs all threads in parallel."""
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
