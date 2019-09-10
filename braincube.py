"""Save parameters formated for braincube"""

# %%
# Imports
import os
import pandas as pd
import datetime as dt
from database import DataBase as db
from helpers import get_newest_inputdate, to_date

# %%
# Initialization
PATH = os.environ['PATH_BRAINCUBE']
DB = os.environ['DB']
LAST_BC_DUMP = to_date(db.get_key_value("braincube_last_save"))
LAST_XFP_EXTRACTION = to_date(db.get_key_value("last_XFP_extraction"))
LAST_XFP_FULL_EXTRACTION = to_date(
    db.get_key_value("last_XFP_full_extraction"))

# %%
# Set extraction date
if LAST_BC_DUMP >= LAST_XFP_EXTRACTION:
    EXTRACTION_DATE = "" # no need to extract anything
if LAST_BC_DUMP < LAST_XFP_FULL_EXTRACTION:
    EXTRACTION_DATE = "1920-01-01 00:00:00" # extract everything
elif LAST_BC_DUMP < LAST_XFP_EXTRACTION:
    EXTRACTION_DATE = LAST_BC_DUMP # partial extract


# %%
# Get all the values
if EXTRACTION_DATE:
    sql = f"""SELECT PO
                    ,family
                    ,area
                    ,parameter
                    ,value
                    ,unit
                    ,inputdate as INPUTDATE
            FROM {DB}.dbo.params_values
            where inputdate >= '{EXTRACTION_DATE}'"""
    df_params = db.select(sql)

    # get process orders
    sql = f"""SELECT process_order
                    ,batch
                    ,material
                    ,description
                    ,launch_date
                    ,strength
              FROM {DB}.dbo.process_orders"""
    df_orders = db.select(sql)
    df_orders = df_orders.loc[df_orders["process_order"].isin(df_params["PO"])]

    # get process stages
    sql = """SELECT * FROM (SELECT
                            substr(a.numlot,0,8) AS baselot,
                            substr(a.codeart,0,8) AS trimcodeart,
                            TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
                            TRIM(CASE
                                WHEN(instr(a.codeart,'-') ) > 1 THEN TO_CHAR(substr(a.codeart, (instr(a.codeart,'-') + 1),length(a.codeart) ) )
                                ELSE 'FINI'
                            END) AS workcentrecode
                        FROM
                            elan2406prd.xfp_lotstraces a
                            INNER JOIN elan2406prd.xfp_articles b ON a.codeart = b.codeart
                        WHERE
                            ( ( fonction LIKE 'PRODUCTION LOT'
                                AND message LIKE 'Manuf%' ) /* OR (FONCTION LIKE 'CONSOMM. AJUSTEMENT')*/ )
                        UNION
                        SELECT
                            substr(a.numlotproduit,0,8) AS baselot,
                            substr(b.codeart,0,8) AS trimcodeart,
                            TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
                            'DISP' AS workcentrecode
                        FROM
                            elan2406prd.xfp_lotstraces a
                            INNER JOIN elan2406prd.xfp_lots b ON a.numlotproduit = b.codelot
                        WHERE
                            ( fonction LIKE 'CONSOMMATION' )
                    ) PIVOT (
                        MIN ( mandecdate )
                    AS transdate
                        FOR workcentrecode
                        IN ( 'DISP', 'G', 'BL', 'T',  'CT', 'P', 'FINI' ))
                union

                SELECT * FROM (SELECT
                            substr(a.numlot,0,8) AS baselot,
                            substr(a.codeart,0,8) AS trimcodeart,
                            TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
                            TRIM(CASE
                                WHEN(instr(a.codeart,'-') ) > 1 THEN TO_CHAR(substr(a.codeart, (instr(a.codeart,'-') + 1),length(a.codeart) ) )
                                ELSE 'FINI'
                            END) AS workcentrecode
                        FROM
                            arch2406prd.xfp_lotstraces a
                            INNER JOIN arch2406prd.xfp_articles b ON a.codeart = b.codeart
                        WHERE
                            ( ( fonction LIKE 'PRODUCTION LOT'
                                AND message LIKE 'Manuf%' ) /* OR (FONCTION LIKE 'CONSOMM. AJUSTEMENT')*/ )
                        UNION
                        SELECT
                            substr(a.numlotproduit,0,8) AS baselot,
                            substr(b.codeart,0,8) AS trimcodeart,
                            TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
                            'DISP' AS workcentrecode
                        FROM
                            arch2406prd.xfp_lotstraces a
                            INNER JOIN arch2406prd.xfp_lots b ON a.numlotproduit = b.codelot
                        WHERE
                            ( fonction LIKE 'CONSOMMATION' )
                    ) PIVOT (
                        MIN ( mandecdate )
                    AS transdate
                        FOR workcentrecode
                        IN ( 'DISP', 'G', 'BL', 'T',  'CT', 'P', 'FINI' ))"""
    df_stages = db.xfp_run_sql(sql)
    df_stages = df_stages.loc[df_stages["BASELOT"].isin(df_orders["batch"])]


    #df_params["value"] = pd.to_numeric(df_params["value"], errors='coerce')
    newest_inputdate = dt.datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S")  # get_newest_inputdate(df_params)
    db.save_key_value("braincube_last_save", newest_inputdate)
    path = PATH + "\\output\\"
    time_now = dt.datetime.today().strftime("%Y%m%d-%H%M")
    filename_param = "\\" + "XFP_parameters-" + time_now + ".csv"
    filename_po = "\\" + "XFP_orders-" + time_now + ".csv"
    filename_stages = "\\" + "process_stages-" + time_now + ".csv"
    print(path + filename_param)
    print(path + filename_po)
    print(path + filename_stages)
    if not os.path.exists(path):
        os.makedirs(path)
    df_params.to_csv(path + filename_param, sep=';', index=False)
    df_orders.to_csv(path + filename_po, sep=';', index=False)
    df_stages.to_csv(path + filename_stages, sep=';', index=False)
    #df_po.to_csv(path + filename_po, sep=';', index=False)


# %%
