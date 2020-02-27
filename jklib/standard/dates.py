# coding: utf-8
"""
Description:
    Contains useful function for handling dates
Functions:
    get_all_dates: Creates a list of tuples with date info for all the dates between 'start' and 'end'
    get_same_date: Returns the 'absolute' equivalent day from the chosen year
    get_same_day: Returns the 'relative' equivalent day with the chosen delta
"""


# Built-in
from datetime import datetime, timedelta

# Third-party
from dateutil.relativedelta import relativedelta


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def get_all_dates(start, end):
    """
    Description:
        Creates a list of tuples with date info for all the dates between 'start' and 'end'
        A tuple contains (year, month, week, day) which are either strings or integers
    Args:
        start (date): start date of the dashboard
        end (date): end date of the dashboard
    Returns:
        list: list of tuples (year, month, week, day)
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


def get_same_date(date, years, format="%Y-%m-%d"):
    """
    Description:
        Returns the 'absolute' equivalent day from the chosen year.
        Absolute means matching 01/01 with 01/01.
    Args
        date (str): string input of a date.
        years (int): number of years between your date and the one you want.
        format (str): output format of the returned date.
    Returns
        date_equiv_format -- corresponding date (with the chosen delta) in the requested format.
    """
    date_format = datetime.strptime(date, "%Y-%m-%d")
    date_equiv = date_format + relativedelta(years=years)
    date_equiv_format = date_equiv.strftime(format)
    return date_equiv_format


def get_same_day(date, years, months=0, days=0, format="%Y-%m-%d"):
    """
    Description:
        Returns the 'relative' equivalent day with the chosen delta
        Relative means matching a Monday with a Monday.
    Args:
        date (str): string input of a date.
        years (int): number of years between your date and the one you want.
        months (int): number of months between your date and the one you want.
        days (int): number of days between your date and the one you want.
        format (str): output format of the returned date.
    Returns
        (str) Corresponding date (with the chosen delta) in the requested format
    """
    date_format = datetime.strptime(date, "%Y-%m-%d")
    date_equiv = date_format + relativedelta(
        years=years, months=months, days=days, weekday=date_format.weekday()
    )
    date_equiv_format = date_equiv.strftime(format)
    return date_equiv_format
