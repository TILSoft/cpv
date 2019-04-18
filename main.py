# %%
import pandas as pd
from xfp import Xfp as xfp
from database import DataBase as db
from myhelpers import format_params_list
from timeit import default_timer as timer

USE_ARCH_DB = False
LAST_EXTRACTION = db.get_last_extraction_time()
#LAST_EXTRACTION = "2019-04-17 10:00:00"
print(LAST_EXTRACTION)

# %%
df_param_list_main = db.get_param_list_main()
df_param_list_taggers = db.get_param_list_taggers()
df_param_list_agg = db.get_param_list_agg()

# %%
# get list of all parameters to be extracted from XFP formated for SQL
df_param_list_column = pd.concat([
    df_param_list_main['parameter'],
    df_param_list_taggers['parameter'],
    df_param_list_agg['parameter']],
    ignore_index=True, sort=False).drop_duplicates().reset_index(drop=True)
format_param_list = format_params_list(df_param_list_column)

# %%

start = timer()
df_params = xfp.get_parameters(format_param_list, LAST_EXTRACTION, USE_ARCH_DB)
end = timer()
print("df_params duration = " + str((end - start) / 60) + " min")
newest_inputdate = xfp.get_newest_inputdate(df_params)
db.save_last_extraction_time(newest_inputdate)
print(newest_inputdate)


# %%


