"""Main file to be executed"""
# pylint: disable=invalid-name
# %%

from timeit import default_timer as timer
import pandas as pd
from xfp import Xfp as xfp
from database import DataBase as db
from myhelpers import format_params_list
from db_excel_upload import excel_upload
pd.options.display.max_columns = None

# %%
start1 = timer()
LAST_EXTRACTION = db.get_last_extraction_time()
# LAST_EXTRACTION = "2019-06-04 09:00:00"
USE_ARCH_DB = False
# Means reread all params data, purge table and pulll ALL the parameters
REDO_EVERYTHING = False
if REDO_EVERYTHING:
    USE_ARCH_DB = True
    db.truncate_all()
    excel_upload()

# %%
# get list of all parameters to be extracted from XFP formated for SQL
df_param_list_main = db.get_param_list_main()
df_param_list_special = db.get_param_list_special()
df_param_list_column = pd.concat([df_param_list_main['parameter'],
                                  df_param_list_special['parameter']],
                                 ignore_index=True, sort=False
                                 ).drop_duplicates().reset_index(drop=True)
format_param_list = format_params_list(df_param_list_column)

# %%
# extract all parameters
start = timer()
df_params = xfp.get_parameters(format_param_list, LAST_EXTRACTION,
                               REDO_EVERYTHING, USE_ARCH_DB)
end = timer()
print("df_params duration = " + str((end - start) / 60) + " min")
newest_inputdate = xfp.get_newest_inputdate(df_params)
db.save_last_extraction_time(newest_inputdate)

# %%
# Prep parameters dataframes
# Filter to include only required parameters
df_param_main_values = df_params.loc[df_params["PARAMETERCODE"].isin(
    df_param_list_main['parameter'])]
df_param_special = df_params.loc[df_params["PARAMETERCODE"].isin(
    df_param_list_special['parameter'])]
df_param_special.head()


# %%
# Get all special parameters to recalculate agg functions
if (not REDO_EVERYTHING) and (not df_param_special.empty):
    format_param_list = format_params_list(df_param_special['PARAMETERCODE'])
    format_wo_list = format_params_list(df_param_special['MANCODE'])
    df_param_special = xfp.get_parameters(
        format_param_list, LAST_EXTRACTION,
        REDO_EVERYTHING, USE_ARCH_DB, special=True)

# %%
# Get process orders
df_orders = xfp.get_orders(USE_ARCH_DB)

# %%
# join with the po table,
# mainly to get the master emi to join the param csv file later
df_param_main_values = pd.merge(df_param_main_values,
                                df_orders,
                                left_on='MANCODE', right_on='PO')

# %%
df_param_main_values.head()
# %%
df_orders.head()
# %%
df_param_list_main.head()

# %%
# join with parameter list to get family name, needed for saving separate files
df_param_main_values = pd.merge(df_param_main_values,
                                df_param_list_main,
                                left_on=['PARAMETERCODE', 'EMI_MASTER'],
                                right_on=['parameter', 'emi_master'])

# %%
# Filter out indexes smaller than max input index
df_param_main_values = df_param_main_values.loc[df_param_main_values.groupby(
    ['MANCODE', 'EMI_MASTER', 'PARAMETERCODE'])["INPUTINDEX"].idxmax()]


# %%
df_param_main_values.head()


# %%
# update db
db.update_params_values(df_param_main_values)

# %%
# summary
print(f"Ther are {df_param_main_values.shape[0]} new records.")
end1 = timer()
print(f"Total execution time = {str(round(((end1 - start1) / 60), 2))} min")

# %%
