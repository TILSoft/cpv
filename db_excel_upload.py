"""It uploads parameters from spreadsheet files to the main db"""

# %%
import os
import pandas as pd
from sqlalchemy.sql import text
from helpers import trim_all_columns
from database import DataBase as db

__DB = os.environ['MYSQL_DB']
# %%


def excel_upload():
    """Main function"""

    db.truncate_tables(False)
    table = f"{__DB}.params_main"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :parameter, :family, :area, :description,
                    :dataformat, :range_min, :range_max)
                    ON DUPLICATE KEY UPDATE
                    family = :family, area = :area,
                    description = :description,
                    dataformat = :dataformat,
                    range_min = :range_min, range_max = :range_max""")
    dataframe = pd.read_excel('input/params_main.xlsx')
    dataframe = trim_all_columns(dataframe)
    db.update(statement, dataframe)

    table = f"{__DB}.params_special"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :emi_parent, :emi_sub,
                    :parameter, :subemi_name, :groupid,
                    :area, :family, :description,
                    :agg_function, :dataformat, :range_min, :range_max)
                    ON DUPLICATE KEY UPDATE
                    groupid = :groupid, family = :family, area = :area,
                    description = :description,
                    dataformat = :dataformat,
                    range_min = :range_min, range_max = :range_max""")
    dataframe = pd.read_excel('input/params_special.xlsx')
    dataframe = trim_all_columns(dataframe)
    db.update(statement, dataframe)
