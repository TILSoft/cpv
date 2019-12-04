# %%
# Imports
import pandas as pd
from database import DataBase as db
from ranges import Ranges
from helpers import format_params_list, get_newest_inputdate
from xfp import Xfp as xfp

#%%
def compare_string(a, b):
    print(type(a))
    print(type(b))
    if a in b:
        return True
    return False

df = df_param_special.loc[df_param_special.apply(lambda row: row['subemi_name'] in row['SUBEMI_TITLE'], axis=1)]
#df_param_special.loc[compare_string(df_param_special["subemi_name"].str.lower(), df_param_special["SUBEMI_TITLE"].str.lower())]
# %%
