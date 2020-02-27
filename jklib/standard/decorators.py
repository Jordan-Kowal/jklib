# coding: utf-8
"""
Description:
    Contains useful decorators
Functions:
    postgresql_connection: Automatically connects to the database before executing a query, and then disconnects
    time_it: Times a function and prints its time in the console
"""


# Built-in
from time import perf_counter

# Third-party
import psycopg2


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def postgresql_connection(func):
    """
    Description:
        Automatically connects to the database before executing a query, and then disconnects
        Used for functions that handle database queries
    Args:
        func (function): The function that will pass a database query
    Returns:
        (any) What the function passed as argument normally returns
    """

    def wrapper(*args, **kwargs):
        """Wrapper that connects and disconnects from the database"""
        connection = psycopg2.connect(host="", database="", user="", password="")
        results = func(connection, *args, **kwargs)
        connection.close
        return results

    return wrapper


def time_it(function):
    """Times a function and prints its time in the console"""

    def run_it(*args, **kwargs):
        time_before = perf_counter()
        results = function(*args, **kwargs)
        time_total = perf_counter() - time_before
        print(f"{function.__name__} : {time_total} seconds")
        return results

    return run_it
