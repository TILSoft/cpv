"""Execute all the queries on the main mysql database"""

# %%
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import cx_Oracle
from myhelpers import trim_all_columns


# %%
class DataBase:
    """Execute all the queries on the main mysql database"""

    __DB = os.environ['MYSQL_DB']
    __PORT = os.environ['MYSQL_PORT']
    __HOST = os.environ['MYSQL_HOST']
    __USERNAME = os.environ['MYSQL_USERNAME']
    __PASSWORD = os.environ['MYSQL_PASSWORD']
    __DB_XFP_SID = os.environ['XFP_DB_SID']
    __DB_XFP_IP = os.environ['XFP_DB_IP']
    __DB_XFP_PORT = os.environ['XFP_DB_PORT']
    __USERNAME_XFP = os.environ['XFP_USERNAME']
    __PASSWORD_XFP = os.environ['XFP_PASSWORD']

    @classmethod
    def update(cls, statement, dataframe):
        """Execute Insert or Update SQL statement on the database"""

        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))

        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                for row in dataframe.itertuples():
                    connection.execute(statement, **row._asdict())
            except Exception as e:
                print(e)
                transaction.rollback()

    @classmethod
    def update_params_values(cls, dataframe):
        """Execute Insert or Update SQL statement on the database"""

        table = f"{cls.__DB}.params_values"
        statement = text(f"""INSERT INTO {table} VALUES (:MANCODE, :family, :area,
                    :description, :VALUE, :dataformat, :INPUTDATE)
                    ON DUPLICATE KEY UPDATE
                    value = :VALUE,
                    unit = :dataformat,
                    inputdate = :INPUTDATE
                    """)
        dataframe = trim_all_columns(dataframe)
        cls.update(statement, dataframe)

    @classmethod
    def select(cls, query):
        """Return dataframe from SQL"""

        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))

        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                dataframe = pd.read_sql(query, connection)
            except Exception as e:
                print(e)
                transaction.rollback()
        return dataframe

    @classmethod
    def get_param_list_main(cls):
        """Get the main parameter table"""

        query = "select * from cpv.params_main"
        return cls.select(query)

    @classmethod
    def get_param_list_special(cls):
        """Get the special parameter table"""

        query = "select * from cpv.params_special"
        return cls.select(query)

    @classmethod
    def get_param_list_agg(cls):
        """Get the aggregate parameter table"""

        query = "select * from cpv.params_aggregate"
        return cls.select(query)

    @classmethod
    def save_last_extraction_time(cls, time):
        """Update the last extraction time"""

        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))
        statement = f"""INSERT into cpv.key_values VALUES ('last_extracted', '{time}')
                            ON DUPLICATE KEY UPDATE value = '{time}';"""
        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                connection.execute(statement)
            except Exception as e:
                print(e)
                transaction.rollback()

    @classmethod
    def get_last_extraction_time(cls):
        """get the last extraction time"""

        query = "select value FROM cpv.key_values where keyname = 'last_extracted'"
        return cls.select(query).iloc[0]["value"]


    @classmethod
    def xfp_run_sql(cls, query):
        """Run select and return dataframe"""
        try:
            connection_string = cx_Oracle.makedsn(cls.__DB_XFP_IP,
                                                  cls.__DB_XFP_PORT,
                                                  cls.__DB_XFP_SID)
            connection = cx_Oracle.connect(cls.__USERNAME_XFP,
                                           cls.__PASSWORD_XFP,
                                           connection_string)
            dataframe = pd.read_sql(query, connection)
        except Exception as e:
            print(e)
            raise
        finally:
            connection.close()

        return dataframe

    @classmethod
    def truncate_all(cls):
        engine = create_engine('mysql://{}:{}@{}/{}'.format(
                cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))
        statements = [f"TRUNCATE TABLE {cls.__DB}.params_values",
                    f"TRUNCATE TABLE {cls.__DB}.params_aggregate",
                    f"TRUNCATE TABLE {cls.__DB}.params_main",
                    f"TRUNCATE TABLE {cls.__DB}.params_taggers"]
        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                for statement in statements:
                    connection.execute(statement)
            except Exception as e:
                print(e)
                transaction.rollback()

