# Things to note

## ENV variables
C:\Users\sobczakk\AppData\Local\Continuum\miniconda3\envs\DMS_interface\etc\conda\

## Oracle connection

    Files needed for the oracle client for the jupyter image from
    https://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html
    instantclient-basic-linux.x64-11.2.0.4.0.zip
    instantclient-sqlplus-linux.x64-11.2.0.4.0.zip
    instantclient-sdk-linux.x64-11.2.0.4.0.zip

    host package unixodbc-dev is needed for "pipenv install pyodbc"

## SQL Server
    follow https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017

## MySQL
    it needs libmysqlclient-dev and python3-dev on the host for sqlalchemy to work

## Jupyter
    due to bug https://github.com/jupyter/notebook/issues/4399, install tornado==5.1.1

## Parameters

- Every parameter must be in the params_main even if it is in other files
- Params_taggers - use to mark subemi using batchids of "taggers" parameters to remove not needed values. Eg is parameter is present in 5 subemis but only values from 3 required
  - From the main file filter out all row which batch id is not the combination of PARAMETERCODE and Target_Param
  - Must be executed before any of the AGG function to drop unnecessary rows
