"""Utility functions for the pandas library."""
# Built-in
from typing import Dict, List, Union

# Third-party
from pandas import DataFrame


def sorted_group_by(
    df: DataFrame,
    sorted_column: str,
    group_by_fields: List[str],
    agg_fields: List[str],
    agg_options: Union[Dict, str],
) -> DataFrame:
    """Will 'group by' and aggregate values in a DataFrame, while keeping a
    specific sort/order."""
    # Creates the sort reference
    uniques = df[sorted_column].unique()
    sorter_index = {value: i for (i, value) in enumerate(uniques)}
    # Aggregates the dataframe
    df = df.groupby(group_by_fields)[agg_fields].agg(agg_options)
    df = df.reset_index()
    # Sorts the dataframe in its original order
    df["sorting_column"] = df[sorted_column].map(sorter_index)
    df = df.sort_values("sorting_column")
    return df
