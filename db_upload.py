"""It uploads parameters from spreadsheet files to the main db"""

# %%
import os
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import myhelpers
# %%
DB = os.environ['MYSQL_DB']
PORT = os.environ['MYSQL_PORT']
HOST = os.environ['MYSQL_HOST']
USERNAME = os.environ['MYSQL_USERNAME']
PASSWORD = os.environ['MYSQL_PASSWORD']
ENGINE = create_engine('mysql://{}:{}@{}/{}'.format(USERNAME, PASSWORD,
                                                    HOST, DB))
# %%


def main():
    """Main function"""

    table = f"{DB}.params_main"
    df_main = pd.read_excel('input/params_main.xlsx')
    connection = ENGINE.connect()
    with connection.begin() as transaction:
        statement = text(f"""INSERT INTO {table}(emi_master, parameter, family,
                        area, description, dataformat) VALUES(:emi_master,
                        :parameter, :family, :area, description,
                        dataformat)""")
        try:
            for row in df_main.itertuples():
                # print(statement.format(emi_master=row.emi_master))
                connection.execute(statement, **row._asdict())
                #transaction.commit()            
        except Exception as e:
            print(e)
            transaction.rollback()
            #raise


# DF_PARAMS_MAIN['code'][3] = "   trim test        "
# DF_PARAMS_MAIN = myhelpers.trim_all_columns(DF_PARAMS_MAIN)
# print(DF_PARAMS_MAIN['code'])


if __name__ == "__main__":
    main()
