"""Select queries on the XFP database"""
# %%
import os
import pandas as pd
import cx_Oracle
# %%


class Xfp:
    """Select queries on the XFP database"""
    __DB_SID = os.environ['XFP_DB_SID']
    __DB_IP = os.environ['XFP_DB_IP']
    __DB_PORT = os.environ['XFP_DB_PORT']
    __USERNAME = os.environ['XFP_USERNAME']
    __PASSWORD = os.environ['XFP_PASSWORD']

    @staticmethod
    def run_sql(sql):
        """Run select and return dataframe"""
        connection_string = cx_Oracle.makedsn(
            Xfp.__DB_IP, Xfp.__DB_PORT, Xfp.__DB_SID)
        connection = cx_Oracle.connect(
            Xfp.__USERNAME, Xfp.__PASSWORD, connection_string)
        dataframe = pd.read_sql(sql, connection)
        return dataframe
