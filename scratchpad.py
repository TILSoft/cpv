# """Main file to be executed"""
# pylint: disable=invalid-name

# %%
# Imports
import os
from distutils.util import strtobool
from timeit import default_timer as timer
import pandas as pd
from database import DataBase as db
from db_excel_upload import excel_upload
from helpers import format_params_list, get_newest_inputdate, trim_all_columns, create_sql_snippet
REDO_EVERYTHING = False
USE_ARCH_DB = False
pd.options.display.max_columns = None
LAST_EXTRACTION = '2019-07-17 06:46:29'
#__LAST_EXTRACTION = "2019-07-04 09:00:00"
format_param_list = ""
format_wo_list = ""

# %%
def get_parameters(params, wos, time, redo, arch_db):
    """Get parameters from XFP"""

    orders = ""
    date_txt = f"""and inputdate >= TO_DATE('{time}',
                    'yyyy-mm-dd hh24:mi:ss')"""
    params = create_sql_snippet("where", "parametercode", params)

    if wos:
        orders = create_sql_snippet("and", "mancode", wos)
    if redo:
        date_txt = ""
    sql_params_prd = f"""select picode as picode, mancode, batchid,
                            parametercode as parametercode, inputindex,
                            inputdate, operationnumber, datatype,
                            numvalue, datevalue,
                            dbms_lob.substr(textvalue,4000,1) as textvalue
                            from ELAN2406PRD.e2s_pidata_man
                            {params}
                            {orders}
                            {date_txt}
                            """

    sql_params_arch = f"""select picode as picode, mancode, batchid,
                            parametercode as parametercode, inputindex,
                            inputdate, operationnumber, datatype,
                            numvalue, datevalue,
                            dbms_lob.substr(textvalue,4000,1) as textvalue
                            from arch2406PRD.e2s_pidata_man
                            {params}
                            {date_txt}
                            """
    print(sql_params_prd)
    df_prd = db.xfp_run_sql(sql_params_prd)

    if arch_db:
        df_arch = db.xfp_run_sql(sql_params_arch)
        df_params = pd.concat([df_prd, df_arch],
                                ignore_index=True,
                                sort=False) \
            .drop_duplicates().reset_index(drop=True)
    else:
        df_params = df_prd.drop_duplicates().reset_index(drop=True)

    # for some reason there are some strange dates in the database
    df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                    (df_params["DATEVALUE"]
                                    .astype(str).str.startswith("0"))].index,
                    inplace=True, axis=0)
    df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                    (df_params["DATEVALUE"]
                                    .astype(str).str.startswith("28"))].index,
                    inplace=True, axis=0)
    df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                    (df_params["DATEVALUE"]
                                    .astype(str).str.startswith("1900"))].index,
                    inplace=True, axis=0)

    # Rounding
    df_params["NUMVALUE"] = df_params["NUMVALUE"].round(2)
    # check and save an actual value
    df_params["VALUE"] = df_params["NUMVALUE"]
    df_params.loc[df_params["DATATYPE"] == 0, "VALUE"] = \
        df_params["TEXTVALUE"]
    df_params.loc[df_params["DATATYPE"] == 2, "VALUE"] = \
        df_params["DATEVALUE"].dt.strftime('%d-%m-%Y %H:%M:%S')

    # drop Null values
    df_params.drop(df_params.loc[df_params["VALUE"].isnull()]
                    .index, inplace=True, axis=0)

    return trim_all_columns(df_params)


# %%
# get list of all parameters to be extracted from XFP formated for SQL
#format_param_list = ["'TIL_CF_DRY_T°C', 'TILE_SAMPLED_QTY'"]
format_param_list = ["'TIL_CF_DRY_T\xb0C', 'TILE_SAMPLED_QTY'"]

format_wo_list = ["'0220960565'"]

# %%
# Extract all parameters
df_params = get_parameters(format_param_list, format_wo_list, LAST_EXTRACTION,
                               REDO_EVERYTHING, USE_ARCH_DB)
print(df_params)


#%%
