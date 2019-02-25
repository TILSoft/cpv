def get_params_list(column):
    """Format the paramter list for the SQL query"""
    params = ""
    for row in column:
        params = params + "'" + row + "',"
    return params[:-1]
