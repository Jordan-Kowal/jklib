"""Utility functions for the pandas library"""


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def sorted_group_by(df, sorted_column, group_by_fields, agg_fields, agg_options):
    """
    Will 'group by' and aggregate values in a DataFrame, while keeping a specific sort/order
    :param DataFrame df: An already sorted dataframe
    :param str sorted_column: The column which unique values we will use as sorting reference
    :param group_by_fields: The fields by which we groupby
    :type group_by_fields: list(str) or str
    :param agg_fields: The fields we will aggregate by
    :type agg_fields: list(str) or str
    :param agg_options: The arguments passed to the .agg() method
    :type agg_fields: dict or str
    :return: The 'grouped by', aggregated, and sorted DataFrame
    :rtype: DataFrame
    """
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
