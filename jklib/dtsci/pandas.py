# coding: utf-8
"""
Contains useful functions for pandas
Functions:
    sorted_groupby: Will groupby and aggregate values in a dataframe, while keeping a specific sort/order
"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def sorted_groupby(df, sorted_column, groupby_fields, agg_fields, agg_options):
    """
    Will groupby and aggregate values in a dataframe, while keeping a specific sort/order
    Args:
        df (DataFrame): An already sorted dataframe
        sorted_column (str): The column which unique values we will use as sorting reference
        groupby_fields (str, list): The fields by which we groupby
        agg_fields (str, list): The fields we will aggregate
        agg_options (str, dict): The arguments passed to the .agg() method
    Returns:
        (DataFrame)
    """
    # Creates the sort reference
    uniques = df[sorted_column].unique()
    sorter_index = {value: i for (i, value) in enumerate(uniques)}
    # Aggregates the dataframe
    df = df.groupby(groupby_fields)[agg_fields].agg(agg_options)
    df = df.reset_index()
    # Sorts the dataframe in its original order
    df["sorting_column"] = df[sorted_column].map(sorter_index)
    df = df.sort_values("sorting_column")
    return df
