# coding: utf-8
"""
Contains useful function for handling dates
Functions:
    get_all_dates: Creates a list of tuples with date info for all the dates between 'start' and 'end'
"""


# Built-in
from datetime import datetime, timedelta


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_all_dates(start, end):
    """
    Creates a list of tuples with date info for all the dates between 'start' and 'end'
    A tuple contains (year, month, week, day) which are either strings or integers
    Args:
        start (date): start date of the dashboard
        end (date): end date of the dashboard
    Returns:
        (list) list of tuples (year, month, week, day)
    """
    months = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Aout",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ]
    # Find all days
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    # Generate tuples
    several_years = True if start.year != end.year else False
    date_list = []
    for date in days:
        year = date.year
        day = date.strftime("%d/%m/%Y")
        # Month
        month = months[date.month - 1]
        if several_years:
            month += " " + str(date.year)
        # Week
        number = date.isocalendar()[1]
        week = "S{:02}".format(number)
        if several_years:
            if date.month == 12 and number == 1:
                week += " " + str(date.year + 1)
            else:
                week += " " + str(date.year)
        date_list.append((year, month, week, day))
    return date_list
