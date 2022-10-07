"""Utility function for handling dates/times of all sorts."""


# Built-in
from datetime import date, timedelta
from typing import List, Tuple


def get_all_dates(start: date, end: date) -> List[Tuple[int, str, str, str]]:
    """Creates a list of tuples with date info for all the dates between
    'start' and 'end' A tuple contains (year, month, week, day) which are
    either strings or integers."""
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    # Find all days
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    # Generate tuples
    several_years = True if start.year != end.year else False
    date_list = []
    for current_day in days:
        year = current_day.year
        day = current_day.strftime("%d/%m/%Y")
        # Month
        month = months[current_day.month - 1]
        if several_years:
            month += " " + str(current_day.year)
        # Week
        number = current_day.isocalendar()[1]
        week = "S{:02}".format(number)
        if several_years:
            if current_day.month == 12 and number == 1:
                week += " " + str(current_day.year + 1)
            else:
                week += " " + str(current_day.year)
        date_list.append((year, month, week, day))
    return date_list
