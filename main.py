# """Main file to be executed"""
# pylint: disable=invalid-name

# %%
# Imports
import os
import datetime
from distutils.util import strtobool
from timeit import default_timer as timer
import pandas as pd
from database import DataBase as db
from db_excel_upload import excel_upload
from helpers import format_params_list, get_newest_inputdate
from xfp import Xfp as xfp

# %%
# initialization
REDO_EVERYTHING = bool(strtobool(os.environ['REDO_EVERYTHING']))
USE_ARCH_DB = bool(strtobool(os.environ['USE_ARCH_DB']))
pd.options.display.max_columns = None
start1 = timer()
LAST_EXTRACTION = db.get_key_value("last_XFP_extraction")
#__LAST_EXTRACTION = "2019-07-04 09:00:00"
format_param_list = ""
format_wo_list = ""

# %%
# Redo?
if REDO_EVERYTHING:
    USE_ARCH_DB = True
    db.truncate_tables()
    excel_upload()

# %%
# get list of all parameters to be extracted from XFP formated for SQL
df_param_list_main = db.get_param_list_main()
df_param_list_special = db.get_param_list_special()
df_param_list_column = pd.concat([df_param_list_main["parameter"],
                                  df_param_list_special["parameter"]],
                                 ignore_index=True, sort=False
                                 ).drop_duplicates().reset_index(drop=True)
format_param_list = format_params_list(df_param_list_column)

# %%
# Get current UTC time
extraction_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# %%
# Extract all parameters
start = timer()
df_params = xfp.get_parameters(format_param_list, format_wo_list, LAST_EXTRACTION,
                               REDO_EVERYTHING, USE_ARCH_DB)
# save last extraction date
db.save_key_value("last_XFP_extraction", extraction_time)

# %%
# Prep parameters dataframes
# Filter to include only required parameters
df_param_main_values = df_params.loc[df_params["PARAMETERCODE"].isin(
    df_param_list_main["parameter"])]
df_param_special = df_params.loc[df_params["PARAMETERCODE"].isin(
    df_param_list_special["parameter"])]
del df_params


# %%
# Get process orders
df_orders = xfp.get_orders(USE_ARCH_DB)

# %%
# Format wo list
if not df_param_special.empty:
    format_wo_list = format_params_list(df_param_special["MANCODE"])
# %%
# Get tasks
if not df_param_special.empty:
    df_tasks_a = xfp.get_tasks(format_wo_list, USE_ARCH_DB)
    # for self merging later to get the parrent emi
    df_tasks_b = df_tasks_a

# %%
# Get all special parameters to recalculate agg functions
if (not REDO_EVERYTHING) and (not df_param_special.empty):
    format_param_list = format_params_list(df_param_special["PARAMETERCODE"], df_param_list_special)
    df_param_special = xfp.get_parameters(
        format_param_list, format_wo_list, LAST_EXTRACTION,
        REDO_EVERYTHING, USE_ARCH_DB)

# %%
# Extraction duration
end = timer()
print("Parameters extraction duration= " + str((end - start) / 60) + " min")

# %%
# Self join tasks to get parent EMI
if not df_param_special.empty:
    df_tasks_self = pd.merge(df_tasks_a, df_tasks_b,
                             left_on=["MANCODE", "MANINDEX", "BATCHID"],
                             right_on=["MANCODE", "MANINDEX", "TASKID"])
    df_tasks_self.rename(columns={"PFCCODE_x": "SUBEMI", "PFCCODE_y": "PARENTEMI",
                                  "TITLE_y": "SUBEMI_TITLE"}, inplace=True)

# %%
# Merge special with tasks to filter based on the task name
if not df_param_special.empty:
    df_param_special = pd.merge(df_tasks_self, df_param_special,
                                left_on=["MANCODE", "ELEMENTID_x", "BATCHID_x", "TASKID_y"],
                                right_on=["MANCODE", "OPERATIONNUMBER", "BATCHID", "BATCHID"])

    # cleanup
    del df_tasks_self, df_tasks_a, df_tasks_b
    df_param_special.drop(["MANINDEX", "TASKID_x", "BATCHID_x",
                           "ELEMENTID_x", "TITLE_x", "TASKID_y",
                           "BATCHID_y", "ELEMENTID_y", "PICODE",
                           "OPERATIONNUMBER", "DATATYPE",
                           "NUMVALUE", "DATEVALUE", "TEXTVALUE"],
                          axis=1, inplace=True)

# %%
# Merge special with orders to get the master emi
if not df_param_special.empty:
    df_param_special = pd.merge(df_param_special, df_orders,
                                left_on="MANCODE", right_on="PO")
    df_param_special = pd.merge(df_param_special, df_param_list_special,
                                left_on=["EMI_MASTER", "PARENTEMI",
                                         "SUBEMI", "PARAMETERCODE"],
                                right_on=["emi_master", "emi_parent",
                                          "emi_sub", "parameter"])
    df_param_special.drop(["PO", "emi_master", "emi_parent",
                           "emi_sub", "parameter", "subemi_name"],
                          axis=1, inplace=True)

# %%
# Filter out indexes smaller than max input index
if not df_param_special.empty:
    df_param_special = df_param_special.loc[df_param_special.groupby(
        ["MANCODE", "EMI_MASTER",
         "PARENTEMI", "SUBEMI",
         "BATCHID", "PARAMETERCODE", "description"])["INPUTINDEX"].idxmax()]

# %%
# Calculate agg values
if not df_param_special.empty:
    df_param_special["VALUE"] = pd.to_numeric( \
        df_param_special["VALUE"], errors='coerce')
    grouped = df_param_special.groupby(["MANCODE", "family", "area", "description", "agg_function", "dataformat", "groupid"])
    df_param_special = grouped.agg({'VALUE': ['min', 'max', 'mean'], "INPUTDATE": 'max'}).reset_index()
    df_param_special.columns = ["MANCODE", "family", "area", "description",
                    "agg_function", "dataformat", "groupid", "MIN", "MAX", "AVG", "INPUTDATE"]
    # select the actual VALUE
    df_param_special["VALUE"] = df_param_special["MIN"]
    df_param_special.loc[df_param_special["agg_function"] == "MAX", "VALUE"] = \
        df_param_special["MAX"]
    df_param_special.loc[df_param_special["agg_function"] == "AVG", "VALUE"] = \
        df_param_special["AVG"]
    df_param_special["VALUE"] = df_param_special["VALUE"].round(2)

# %%
# Save special parameters to the database
if not df_param_special.empty:
    db.update_params_values(df_param_special)
    db.update_process_orders(df_orders.loc[df_orders["PO"].isin(df_param_special["MANCODE"])])

# %%
# Join with the po table,
# mainly to get the master emi to join the param csv file later
df_param_main_values = pd.merge(df_param_main_values,
                                df_orders,
                                left_on="MANCODE", right_on="PO")

# %%
# Join with parameter list to get family name, needed for saving separate files
df_param_main_values = pd.merge(df_param_main_values,
                                df_param_list_main,
                                left_on=["PARAMETERCODE", "EMI_MASTER"],
                                right_on=["parameter", "emi_master"])

# %%
# Filter out indexes smaller than max input index,
# INPUTDATE as not grouping by batchid
df_param_main_values = df_param_main_values.loc[df_param_main_values.groupby(
    ["MANCODE", "EMI_MASTER", "PARAMETERCODE"])["INPUTDATE"].idxmax()]


# %%
# Update db
db.update_params_values(df_param_main_values)
db.update_process_orders(df_orders.loc[df_orders["PO"].isin(df_param_main_values["MANCODE"])])

# %%
# Summary
currentDT = datetime.datetime.now()
print(f"There are {df_param_main_values.shape[0]} new normal records.")
print(f"There are {df_param_special.shape[0]} new special records.")
end1 = timer()
print(f"Total execution time = {str(round(((end1 - start1) / 60), 2))} min")
with open("log.txt", "a+") as text_file:
    print(
        currentDT.strftime("%Y-%m-%d %H:%M:%S") +
        f" - {df_param_main_values.shape[0]} new normal records, " +
        f"{df_param_special.shape[0]} new special records. Total time: " +
        f"{str(round(((end1 - start1) / 60), 2))} min",
        file=text_file)
#%%
