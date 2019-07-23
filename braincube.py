"""Save parameters formated for braincube"""

# %%
# Imports
import os
import pandas as pd
from database import DataBase as db
from helpers import get_newest_inputdate, to_date

# %%
# Initialization
PATH = os.environ['PATH_BRAINCUBE']
LAST_BC_SAVE = to_date(db.get_key_value("braincube_last_save"))
LAST_XFP_EXTRACTION = to_date(db.get_key_value("last_XFP_extraction"))

# %%
# Get all the values
sql = """SELECT v.PO, v.family, v.area, v.parameter, v.value,
         o.batch, o.material, o.description, o.launch_date
         FROM cpv.params_values v, cpv.process_orders o
         where v.po = o.process_order"""
df_params = db.select(sql)
df_params["value"] = pd.to_numeric(
    df_params["value"], errors='coerce')
df_params.head()


# %%
# Save extraction date
newest_inputdate = get_newest_inputdate(df_params)
db.save_key_value("braincube_last_save", newest_inputdate)
