"""Execute all the queries on the main mysql database"""

# %%
import os
from sqlalchemy import create_engine
import pandas as pd
import cx_Oracle

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
    def get_param_list_taggers(cls):
        """Get the taggers parameter table"""

        query = "select * from cpv.params_taggers"
        return cls.select(query)

    @classmethod
    def get_param_list_agg(cls):
        """Get the aggregate parameter table"""

        query = "select * from cpv.params_aggregate"
        return cls.select(query)

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
