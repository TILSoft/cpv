# %%
import pandas as pd
from database import DataBase as db
from helpers import create_sql_snippet, is_string_digit
from xfp import Xfp as xfp

# %%
# get all spec parameters values
df_main = df_param_main_values


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
df_values.head()

# %%
# query xfp db
df_values = xfp.get_parameters(redo=False, df=df_values)

# take only parameters values entered last in the given batchid
df_values = df_values.loc[df_values.groupby(
    ["MANCODE", "BATCHID", "PARAMETERCODE"])["INPUTINDEX"].idxmax()]

df_values.head()

#%%
df_param_main_values.loc[df_param_main_values["PARAMETERNAME"]]
