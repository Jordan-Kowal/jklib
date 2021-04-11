"""Utility functions and classes for threads"""


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
