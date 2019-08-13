# %%
import pandas as pd

# %%
def create_sql_snippet_html(df):
        """Create sql text"""

        # # only get EMI html if CMDTEXT is empty
        # df = df.loc[df["CMDTEXT"].isnull(),  ["MANCODE", "BATCHID",
        #                 "OPERATIONNUMBER"]].drop_duplicates()

        txt = ""
        for row in df.itertuples():
            print(row)
            txt += (f"or (codefab = '{row.MANCODE}' "
                    f"and batchid = '{row.BATCHID}' "
                    f"and numoperation = '{row.OPERATIONNUMBER}' "
                    f"and inputindex = '{row.BROWSINGINDEX}')\n ")
        return "(" + txt[3:-1] + ")"


create_sql_snippet_html(df_param_special)


#%%
df = pd.concat([
        df_param_special.loc[df_param_special["value_min"].notna(), ["MANCODE", "BATCHID",
                                                                     "value_min"]].rename(columns={"value_min": "value"}),
        df_param_special.loc[df_param_special["value_max"].notna(), ["MANCODE", "BATCHID",
                                                                     "value_max"]].rename(columns={"value_max": "value"}),
        df_param_special.loc[df_param_special["tolerance_min"].notna(), ["MANCODE", "BATCHID",
                                                                         "tolerance_min"]].rename(columns={"tolerance_min": "value"}),
        df_param_special.loc[df_param_special["tolerance_max"].notna(), ["MANCODE", "BATCHID",
                                                                         "tolerance_max"]].rename(columns={"tolerance_max": "value"})], ignore_index=True, sort=False).drop_duplicates()

#%%
#get only parameters
def is_string_digit(value):
    """
    Returns True if string is a number.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


#%%
df_param_special.loc[df_param_special["MANCODE"] == "0220864937", "value_min"] = "45.456"


#%%
def create_sql_snippet_new(keyword, labels, df):
        """Create sql text, order of labels and columns must align"""

        txt = ""
        for row in df.itertuples():
            txt_temp = ""
            for i, label in enumerate(labels, start=1):
                txt_temp += f"and {label} = '{row[i]}'"
            txt = txt + txt_temp[4:]
            txt += f")\nor ("
        return f"{keyword} ({txt[:-5]})"


sql = create_sql_snippet_new(
    "or", df.columns, df.loc[df["MANCODE"] == "OF01077871"])
print(sql)


#%%
from xfp import Xfp as xfp
from helpers import is_string_digit
def params_to_values(df_main, redo):
        """Extracts parameters and saves actual values"""

        # get all spec parameters values
        df_values = pd.concat([
            df_main.loc[df_main["value_min"].notna(), ["MANCODE", "BATCHID",
                                                                         "value_min"]].rename(columns={"value_min": "value"}),
            df_main.loc[df_main["value_max"].notna(), ["MANCODE", "BATCHID",
                                                                         "value_max"]].rename(columns={"value_max": "value"}),
            df_main.loc[df_main["tolerance_min"].notna(), ["MANCODE", "BATCHID",
                                                                             "tolerance_min"]].rename(columns={"tolerance_min": "value"}),
            df_main.loc[df_main["tolerance_max"].notna(), ["MANCODE", "BATCHID",
                                                                             "tolerance_max"]].rename(columns={"tolerance_max": "value"})],
                                                                             sort=False).drop_duplicates()

        # drop all but parameter names
        df_values.dropna(subset=["value"], inplace=True)
        df_values = df_values.loc[~df_values["value"].apply(is_string_digit)]

        # query xfp db
        df_values = xfp.get_parameters(redo=redo, df=df_values)

        # take only parameters values entered last in the given batchid
        df_values = df_values.loc[df_values.groupby(
            ["MANCODE", "BATCHID", "PARAMETERCODE"])["INPUTINDEX"].idxmax()]

        try:
                # go thrugh each spec parameter and replace it with an actual value
                for row in df_main.itertuples():
                        for col in ["value_min", "value_max", "tolerance_min", "tolerance_max"]:
                                spec_param = df_main.at[row.Index, col]
                                if (spec_param is not None) and (not is_string_digit(spec_param)):
                                        value = df_values.loc[(df_values["MANCODE"] == row.MANCODE)
                                                & (df_values["BATCHID"] == row.BATCHID)
                                                & (df_values["PARAMETERCODE"] == spec_param),
                                                "VALUE"].iloc[0]
                                        df_main.at[row.Index, col] = value
        except IndexError as e:
                print(e)
                print(row)
                raise

        return df_main

#%%
df = params_to_values(df_param_special, False)
df_values = df_param_special


# %%
df.loc[df.groupby(
    ["MANCODE", "BATCHID", "PARAMETERCODE"])["INPUTINDEX"].idxmax()]


#%%
df.loc[(df["MANCODE"] == "0220959701") & (df["BATCHID"] == 25412946)]

#%%
df_values.loc[(df_values["MANCODE"] == "0220959701") & (df_values["BATCHID"] == 25412946)]


#%%


df_values.head(20)


#%%
df.loc[(df["MANCODE"] == '0220959701')
       & (df["BATCHID"] == 25412946)]

#%%
df.loc[(df["MANCODE"] == '0220960956')
       & (df["BATCHID"] == 25580431)
       & (df["PARAMETERCODE"] == df_values.at[279, "value_min"]), "VALUE"].iloc[0]



#%%
df.loc[(df["MANCODE"] == '0220960956')
       & (df["BATCHID"] == 25580431)
       & (df["PARAMETERCODE"] == df_values.at[279, "value_min"])]


#%%
