"""Saving csv files for the APR"""
# pylint: disable=invalid-name
# %%
# Imports
import datetime as dt
import os
import pandas as pd
from database import DataBase as db


# %%
# Get all the values
PATH = os.environ['PATH_APR']
sql = """SELECT o.batch, v.PO, o.material, o.description,
		 v.family, v.area, v.parameter, v.value, o.launch_date
         FROM cpv.dbo.params_values v, cpv.dbo.process_orders o
         where v.po = o.process_order"""
df_params = db.select(sql)
df_params["value"] = pd.to_numeric(
    df_params["value"], errors='coerce')
df_params.head()

#%%
# Save Files
def save_files(path_base):
    """Saves  csv files to disk"""
    products = df_params.loc[:, "family"].unique()
    for product in products:
        df = df_params.loc[df_params['family'] == product]
        df = pd.pivot_table(df, values='value',
                            index=['PO', 'batch', 'material',
                                   'description', 'family',
                                   'launch_date'], columns=['parameter'])
        #sort clumns
        cols = sorted(df.columns.tolist())
        df = df[cols]
        path = path_base + "\\output\\" + product
        filename = "\\" + product + " - " + \
            dt.datetime.today().strftime("%Y%m%d %H%M") + ".xlsx"
        print(path + filename)
        if not os.path.exists(path):
            os.makedirs(path)
        df.to_excel(path + filename)


#%%
save_files(PATH)

#%%
