"""Execute all the queries on the main mysql database"""
# pylint: disable=broad-except
# %%
import os
#import codecs
from sqlalchemy import create_engine
from sqlalchemy.sql import text, null
import pandas as pd
import cx_Oracle
from helpers import trim_all_columns


# %%
class DataBase:
    """DB connections"""
    __DB = os.environ['DB']
    __PORT = os.environ['PORT']
    __HOST = os.environ['HOST']
    __USERNAME = os.environ['USERNAME']
    __PASSWORD = os.environ['PASSWORD']
    __DB_XFP_SID = os.environ['XFP_DB_SID']
    __DB_XFP_IP = os.environ['XFP_DB_IP']
    __DB_XFP_PORT = os.environ['XFP_DB_PORT']
    __USERNAME_XFP = os.environ['XFP_USERNAME']
    __PASSWORD_XFP = os.environ['XFP_PASSWORD']

    @classmethod
    def get_engine(cls):
        """"Returns database engin"""
        return create_engine(
            f"mssql+pyodbc://{cls.__USERNAME}:{cls.__PASSWORD}@{cls.__HOST}:{cls.__PORT}/{cls.__DB}?driver=ODBC+Driver+17+for+SQL+Server",
            isolation_level="READ COMMITTED")

    @classmethod
    def update(cls, statement, dataframe):
        """Execute Insert or Update SQL statement on the database"""
        dataframe = dataframe.fillna(value=null())
        dataframe = trim_all_columns(dataframe)
        engine = cls.get_engine()
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
        table = f"{cls.__DB}.dbo.params_values"

        statement = text(f"""MERGE {table} AS target USING
            (SELECT :MANCODE,
                    :family,
                    :area,
                    :description,
                    :VALUE,
                    :dataformat,
                    :INPUTDATE,
                    :value_min,
                    :value_max,
                    :tolerance_min,
                    :tolerance_max) AS source
                (PO,
                    family,
                    area,
                    parameter,
                    VALUE,
                    unit,
                    inputdate,
                    value_min,
                    value_max,
                    tolerance_min,
                    tolerance_max)
            ON (source.PO = target.PO and
                source.family = target.family and
                source.area = target.area and
                source.parameter = target.parameter)
            WHEN MATCHED
                THEN UPDATE SET
                        target.unit = source.unit,
                        target.inputdate = source.inputdate,
                        target.value_min = source.value_min,
                        target.value_max = source.value_max,
                        target.tolerance_min = source.tolerance_min,
                        target.tolerance_max = source.tolerance_max
            WHEN NOT MATCHED by target
                THEN INSERT VALUES
                    (:MANCODE,
                    :family,
                    :area,
                    :description,
                    :VALUE,
                    :dataformat,
                    :INPUTDATE,
                    :value_min,
                    :value_max,
                    :tolerance_min,
                    :tolerance_max);""")
        cls.update(statement, dataframe)

    @classmethod
    def update_process_orders(cls, dataframe):
        """Execute Insert or Update SQL statement on the database"""
        table = f"{cls.__DB}.dbo.process_orders"
        statement = text(f"""MERGE {table} AS target USING
                    (SELECT :PO,
                            :BATCH,
                            :MATERIAL,
                            :DESCRIPTION,
                            :PO_LAUNCHDATE,
                            :ORDER_QTY,
                            :UNIT,
                            :STRENGTH) AS source
                        (process_order,
                            batch,
                            material,
                            description,
                            launch_date,
                            order_quantity,
                            order_unit,
                            strength)
                    ON (source.process_order = target.process_order)
                    WHEN MATCHED
                        THEN UPDATE SET
                            target.batch = source.batch,
                            target.material = source.material,
                            target.description = source.description,
                            target.launch_date = source.launch_date,
                            target.order_quantity = source.order_quantity,
                            target.order_unit = source.order_unit,
                            target.strength = source.strength
                    WHEN NOT MATCHED by target
                        THEN INSERT VALUES
                            (:PO,
                            :BATCH,
                            :MATERIAL,
                            :DESCRIPTION,
                            :PO_LAUNCHDATE,
                            :ORDER_QTY,
                            :UNIT,
                            :STRENGTH);""")
        cls.update(statement, dataframe)

    @classmethod
    def select(cls, query):
        """Return dataframe from SQL"""
        engine = cls.get_engine()
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
        query = f"select * from {cls.__DB}.dbo.params_main"
        return cls.select(query)

    @classmethod
    def get_param_list_special(cls):
        """Get the special parameter table"""
        query = f"select * from {cls.__DB}.dbo.params_special"
        return cls.select(query)

    @classmethod
    def save_key_value(cls, key, value):
        """Update the last extraction time"""

        statement = text(f"""MERGE {cls.__DB}.dbo.key_values AS target USING
                    (SELECT :key, :value) AS source
                        (keyname, value)
                    ON (source.keyname = target.keyname)
                    WHEN MATCHED
                        THEN UPDATE SET
                            target.value = source.value
                    WHEN NOT MATCHED by target
                        THEN INSERT VALUES
                            (:key, :value);""")
        engine = cls.get_engine()
        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                connection.execute(
                    statement, key=key, value=value)
            except Exception as e:
                print(e)
                transaction.rollback()

    @classmethod
    def get_key_value(cls, key):
        """get the last extraction time"""
        query = f"select value FROM {cls.__DB}.dbo.key_values where keyname = \
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

            # with codecs.open('testdata\Failed.txt', 'w', "utf-8") as file:
            #     file.write(query)


            col_names = [row[0] for row in cursor.description]
            dataframe = pd.DataFrame(cursor.fetchall(), columns=col_names)
        except cx_Oracle.DatabaseError as e:
            print(e)
            print(query)
            raise
        finally:
            connection.close()
        return trim_all_columns(dataframe)

    @classmethod
    def truncate_tables(cls, values_also=True):
        """When doing full upload delete all rows before insert"""
        engine = cls.get_engine()
        statements = [f"TRUNCATE TABLE {cls.__DB}.dbo.params_special",
                      f"TRUNCATE TABLE {cls.__DB}.dbo.params_main",
                      f"TRUNCATE TABLE {cls.__DB}.dbo.process_orders"]
        if values_also:
            statements.append(f"TRUNCATE TABLE {cls.__DB}.dbo.params_values")
        connection = engine.connect()
        with connection.begin() as transaction:
            try:
                for statement in statements:
                    connection.execute(statement)
            except Exception as e:
                print(e)
                transaction.rollback()
