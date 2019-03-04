# Helper functions

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
    def trim(x):
        return x.strip() if type(x) is str else x
    return dataframe.applymap(trim)
