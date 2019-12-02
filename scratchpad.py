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
from ranges import Ranges
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
param_list = ""
wo_list = ""

# %%
# Redo?
if REDO_EVERYTHING:
    USE_ARCH_DB = True
    LAST_EXTRACTION = None
    db.truncate_tables(True, False)
    excel_upload()

# %%