"""It uploads parameters from spreadsheet files to the main db"""

# %%
import os
import pandas as pd
from sqlalchemy.sql import text
from myhelpers import trim_all_columns
from database import DataBase as db

__DB = os.environ['MYSQL_DB']

# %%


def main():
    """Main function"""

    table = f"{__DB}.params_main"
    statement = text(f"""INSERT INTO {table}(emi_master, parameter, family,
                    area, description, dataformat) VALUES(:emi_master,
                    :parameter, :family, :area, :description,
                    dataformat) ON DUPLICATE KEY UPDATE
                    family = :family, area = :area, description = :description,
                    dataformat = :dataformat""")
    df_main = pd.read_excel('input/params_main.xlsx')
    df_main = trim_all_columns(df_main)
    db.update(statement, df_main)


if __name__ == "__main__":
    main()
