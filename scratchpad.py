import os
#import codecs
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import cx_Oracle
from helpers import trim_all_columns


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


def get_engine():
    """"Returns database engin"""
    return create_engine(
        f"mssql+pyodbc://{__USERNAME}:{__PASSWORD}@{__HOST}:{__PORT}/{__DB}?driver=ODBC+Driver+17+for+SQL+Server",
        isolation_level="READ COMMITTED")

def update(statement, dataframe):
    """Execute Insert or Update SQL statement on the database"""
    dataframe = trim_all_columns(dataframe)
    dataframe = dataframe.fillna(value="")
    engine = get_engine()
    connection = engine.connect()
    connection.fast_executemany = False
    with connection.begin() as transaction:
        try:
            for row in dataframe.itertuples():
                print(row)
                connection.execute(statement, **row._asdict())
        except Exception as e:
            print(e)
            transaction.rollback()


def update_params_values(dataframe):
        """Execute Insert or Update SQL statement on the database"""
        table = f"{__DB}.dbo.params_values"
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
        update(statement, dataframe)

