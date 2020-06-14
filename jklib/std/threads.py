# coding: utf-8
"""
Functions to deal with threads
Classes:
    BasicThread: Basic thread class to use threads with an action attribute
Functions:
    run_all_threads: Runs all the generated threads at once, and then joins them
"""


# Built-in
from threading import Thread


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class BasicThread(Thread):
    """Basic thread class to use threads with an action attribute"""

    # ----------------------------------------
    # Magic methods
    # ----------------------------------------
    def __init__(self, action):
        """The action param can be used to choose different run methods"""
        Thread.__init__(self)
        self.action = action

    # ----------------------------------------
    # Public methods
    # ----------------------------------------
    def run(self):
        """Runs the thread"""
        if self.action == "":
            pass
        elif self.action == "":
            pass
        else:
            pass


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def run_all_threads(threads):
    """
    Runs all the generated threads at once, and then joins them
    Args:
        threads (list): List of Thread instances we want to run
    """
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
