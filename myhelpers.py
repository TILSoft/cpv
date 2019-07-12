""" Helper functions """

# %%


def format_params_list(column):
    """Format the parameter list for the SQL query"""
    params = ""
    for row in column:
        params = params + "'" + row + "',"
    return params[:-1]


def trim_all_columns(dataframe):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    def trim(value):
        return value.strip() if isinstance(value, str) else value
    return dataframe.applymap(trim)
