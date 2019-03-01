# It uploads parameters from spreadsheet files to the main db

# %%
import pandas as pd
import myhelpers

df_params_main = pd.read_excel('input/params_main.xlsx')

df_params_main['code'][3] = "   trim test        "
df_params_main = myhelpers.trim_all_columns(df_params_main)
print(df_params_main['code'])

