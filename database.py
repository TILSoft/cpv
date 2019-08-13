"""Execute all the queries on the main mysql database"""
# pylint: disable=broad-except
# %%
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import cx_Oracle
from helpers import trim_all_columns


# %%
class DataBase:
    """DB connections"""

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
        statement = text(f"""INSERT INTO {table}
                             VALUES (:MANCODE, :family, :area,
                    :description, :VALUE, :dataformat, :INPUTDATE, :value_min,
                    :value_max, :tolerance_min, :tolerance_max)
                    ON DUPLICATE KEY UPDATE
                    value = :VALUE,
                    unit = :dataformat,
                    inputdate = :INPUTDATE,
                    value_min = :value_min,
                    value_max = :value_max,
                    tolerance_min = :tolerance_min,
                    tolerance_max = :tolerance_max
                    """)
        dataframe = trim_all_columns(dataframe)
        cls.update(statement, dataframe)

    @classmethod
    def update_process_orders(cls, dataframe):
        """Execute Insert or Update SQL statement on the database"""

        table = f"{cls.__DB}.process_orders"
        statement = text(f"""INSERT INTO {table} VALUES (:PO, :BATCH, :MATERIAL,
                    :DESCRIPTION, :PO_LAUNCHDATE, :ORDER_QTY, :UNIT)
                    ON DUPLICATE KEY UPDATE
                    batch = :BATCH,
                    material = :MATERIAL,
                    description = :DESCRIPTION,
                    launch_date = :PO_LAUNCHDATE,
                    order_quantity = :ORDER_QTY,
                    order_unit = :UNIT
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

        query = f"select * from {cls.__DB}.params_main"
        return cls.select(query)

    @classmethod
    def get_param_list_special(cls):
        """Get the special parameter table"""

        query = f"select * from {cls.__DB}.params_special"
        return cls.select(query)

    @classmethod
    def save_key_value(cls, key, value):
        """Update the last extraction time"""

        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))
        statement = f"""INSERT into {cls.__DB}.key_values VALUES ('{key}', '{value}')
                            ON DUPLICATE KEY UPDATE value = '{value}';"""
        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                connection.execute(statement)
            except Exception as e:
                print(e)
                transaction.rollback()
                sys.exit(1)

    @classmethod
    def get_key_value(cls, key):
        """get the last extraction time"""

        query = f"select value FROM {cls.__DB}.key_values where keyname = \
                '{key}'"
        return cls.select(query).iloc[0]["value"]

    @classmethod
    def xfp_run_sql(cls, query):
        """Runs select and returns dataframe"""
        # https://stackoverflow.com/questions/49288724/read-and-write-clob-data-using-python-and-cx-oracle
        def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
            if defaultType == cx_Oracle.CLOB:
                return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
            elif defaultType == cx_Oracle.BLOB:
                return cursor.var(cx_Oracle.LONG_BINARY, arraysize=cursor.arraysize)

        try:
            connection_string = cx_Oracle.makedsn(cls.__DB_XFP_IP,
                                                  cls.__DB_XFP_PORT,
                                                  cls.__DB_XFP_SID)
            connection = cx_Oracle.connect(cls.__USERNAME_XFP,
                                           cls.__PASSWORD_XFP,
                                        connection_string, encoding="UTF-8", nencoding="UTF-8")
            connection.outputtypehandler = OutputTypeHandler
            cursor = connection.cursor()
            cursor.execute(query)
            col_names = [row[0] for row in cursor.description]
            dataframe = pd.DataFrame(cursor.fetchall(), columns=col_names)
        except cx_Oracle.DatabaseError as e:
            print(e)
            print(query)
            raise
            sys.exit(1)
        finally:
            connection.close()
        return trim_all_columns(dataframe)

    @classmethod
    def truncate_tables(cls, values_also=True):
        """When doing full upload delete all rows before insert"""
        engine = create_engine('mysql://{}:{}@{}/{}'.format(
            cls.__USERNAME, cls.__PASSWORD, cls.__HOST, cls.__DB))

        statements = [f"TRUNCATE TABLE {cls.__DB}.params_special",
                      f"TRUNCATE TABLE {cls.__DB}.params_main",
                      f"TRUNCATE TABLE {cls.__DB}.process_orders"]

        if values_also:
            statements.append(f"TRUNCATE TABLE {cls.__DB}.params_values")

        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                for statement in statements:
                    connection.execute(statement)
            except Exception as e:
                print(e)
                transaction.rollback()
                sys.exit(1)
