# %%
import os
import datetime
from distutils.util import strtobool
from timeit import default_timer as timer
import pandas as pd
from database import DataBase as db
from ranges import Ranges
from db_excel_upload import excel_upload
from helpers import format_params_list, get_newest_inputdate
from xfp import Xfp as xfp

# %%
# Get process orders
df_orders = xfp.get_orders(True)

db.update_process_orders(df_orders)


#%%
