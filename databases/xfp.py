# %%
import pandas as pd

import cx_Oracle
import credentials


# %%
class xfp:
    __DB_SID = credentials.XFP_DB_SID
    __DB_IP = credentials.XFP_DB_IP
    __DB_PORT = credentials.XFP_DB_PORT
    __USERNAME = credentials.XFP_USERNAME
    __PASSWORD = credentials.XFP_PASSWORD

    @staticmethod
    def run_sql(sql):
        connectionString = cx_Oracle.makedsn(
            xfp.__DB_IP, xfp.__DB_PORT, xfp.__DB_SID)
        connection = cx_Oracle.connect(
            xfp.__USERNAME, xfp.__PASSWORD, connectionString)
        dataframe = pd.read_sql(sql, connection)
        return dataframe
