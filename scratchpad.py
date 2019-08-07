# %%
import importlib
import os

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import cx_Oracle
import xfp
from helpers import trim_all_columns
importlib.reload(xfp)
from xfp import Xfp as xfp
import ranges
importlib.reload(ranges)
from ranges import Ranges as ranges

# %%
sql_text = ranges.create_sql_snippet_html(df_param_special)
df_html = xfp.get_html(sql_text, False)
df_html.head()

# %%
# Adding new columns
df_param_special["value_min"] = ""
df_param_special["value_max"] = ""
df_param_special["tolerance_min"] = ""
df_param_special["tolerance_max"] = ""

# %%
with open("testdata\\xfp params html example.html", "r", encoding='utf-8') as myfile:
    html = myfile.read();
print(ranges.get_values(html, 94))


# %%
for row in df_param_special.itertuples():
    html = df_html.loc[(df_html["MANCODE"] == row.MANCODE)
                       & (df_html["BATCHID"] == row.BATCHID)
                       & (df_html["OPERATIONNUMBER"] == row.OPERATIONNUMBER),
                       "HTML"].iloc[0]
    values = ranges.get_values(html, row.TAGNUMBER)
    df_param_special.at[row.Index, "value_min"] = values[0]
    df_param_special.at[row.Index, "value_max"] = values[1]
    df_param_special.at[row.Index, "tolerance_min"] = values[2]
    df_param_special.at[row.Index, "tolerance_max"] = values[3]


# %%
html = df_html.loc[(df_html["MANCODE"] == "0220963938")
            & (df_html["BATCHID"] == 25554555) & (df_html["OPERATIONNUMBER"] == 3),
            "HTML"].iloc[0]
print(html)

# %%
df_html.head()

# %%
df_param_special.head()

# %%
print(df_html.HTML[0])


#%%
