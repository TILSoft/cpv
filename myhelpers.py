""" Helper functions """

# %%

def format_params_list(column, df_special=None):
    """
    Format the parameter list for the SQL query
    """
    params = ""
    column = column.unique()
    if df_special is not None:
        groups = df_special.loc[df_special["parameter"].isin(column), "groupid"]
        column = df_special.loc[df_special["groupid"].isin(groups), "parameter"]
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
