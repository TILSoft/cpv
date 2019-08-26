"""It uploads parameters from spreadsheet files to the main db"""

# %%
import os
import pandas as pd
from sqlalchemy.sql import text
from database import DataBase as db

__DB = os.environ['DB']
# %%


def excel_upload():
    """Main function"""

    db.truncate_tables(False)

    table = f"{__DB}.dbo.params_main"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :parameter, :family, :area, :description,
                    :dataformat)
                    """)

    dataframe = pd.read_excel('input/params_main.xlsx')
    db.update(statement, dataframe)

    table = f"{__DB}.dbo.params_special"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :emi_parent, :emi_sub,
                    :parameter, :subemi_name, :description, :groupid,
                    :area, :family,
                    :agg_function, :dataformat)""")

    dataframe = pd.read_excel('input/params_special.xlsx')
    db.update(statement, dataframe)
