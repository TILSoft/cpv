"""It uploads parameters from spreadsheet files to the main db"""

# %%
import os
import pandas as pd
from sqlalchemy.sql import text
from myhelpers import trim_all_columns
from database import DataBase as db

__DB = os.environ['MYSQL_DB']
# %%


def excel_upload():
    """Main function"""

    table = f"{__DB}.params_main"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :parameter, :family, :area, :description,
                    :dataformat) ON DUPLICATE KEY UPDATE
                    family = :family, area = :area,
                    description = :description,
                    dataformat = :dataformat""")
    df = pd.read_excel('input/params_main.xlsx')
    df = trim_all_columns(df)
    db.update(statement, df)

    table = f"{__DB}.params_taggers"
    statement = text(f"""INSERT INTO {table} VALUES (:emi_master,
                    :emi_parent, :emi_sub,
                    :parameter, :task, :area, :family)
                    ON DUPLICATE KEY UPDATE
                    family = :family, area = :area""")
    df = pd.read_excel('input/params_taggers.xlsx')
    df = trim_all_columns(df)
    db.update(statement, df)

    table = f"{__DB}.params_aggregate"
    statement = text(
        f"""INSERT INTO {table} VALUES (:emi_master, :emi_parent, :emi_sub,
                    :parameter, :groupid, :family, :area, :description,
                    :agg_function, :dataformat) ON DUPLICATE KEY UPDATE
                    groupid = :groupid,
                    family = :family,
                    area = :area,
                    description = :description,
                    agg_function = :agg_function,
                    dataformat = :dataformat
                    """)
    df = pd.read_excel('input/params_aggregate.xlsx')
    df = trim_all_columns(df)
    db.update(statement, df)


# if __name__ == "__main__":
#     main()
