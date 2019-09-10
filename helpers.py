""" Helper functions """

# %%


def create_sql_snippet(keyword, labels, df):
    """Create sql text, order of labels and columns must align"""

    txt = ""
    for row in df.itertuples():
        txt_temp = ""
        for i, label in enumerate(labels, start=1):
            txt_temp += f" and {label} = '{row[i]}'"
        txt = txt + txt_temp[4:]
        txt += f")\nor ("
    return f"{keyword} (({txt[:-5]})"


def is_string_digit(value):
    """
    Returns True if string is a number.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def format_params_list(column, df_special=None):
    """
    Format the parameter list for the SQL query,
    Note the Oracle max list size is 1000 elements
    """
    params = ""
    list1000 = []
    column = column.unique()
    # need to get all other parameters from the same group
    if df_special is not None:
        groups = df_special.loc[df_special["parameter"].isin(column), "groupid"]
        column = df_special.loc[df_special["groupid"].isin(groups), "parameter"]
    for counter, row in enumerate(column, 1):
        params = params + "'" + row + "',"
        if (column.size > 1000) and (counter % 1000 == 0):
            params = params[:-1]
            list1000.append(params)
            params = ""
    params = params[:-1]
    list1000.append(params)
    if list1000[0] == "":
        return None
    return list1000

def create_sql_list(keyword, prefix, values):
    """
    Due to Oracle 1000 elemets list limitation,
    any sql list must be divided into smaller pieces
    """
    txt = ""
    for value in values:
        txt = txt + f"{prefix} in ({value}) or "
    return keyword + " (" + txt[:-4] + ")\n"

def trim_all_columns(dataframe):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    def trim(value):
        return value.strip() if isinstance(value, str) else value
    return dataframe.applymap(trim)

def get_newest_inputdate(dataframe):
    """Finds the newest date parameter index was created"""
    return dataframe.loc[:, "INPUTDATE"].max().strftime("%Y-%m-%d %H:%M:%S")

def to_date(textdate):
    """Convert string to a date"""
    from datetime import datetime

    datetime_object = datetime.strptime(
        textdate, "%Y-%m-%d %H:%M:%S")
    return datetime_object


#%%
