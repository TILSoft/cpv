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
PROCESS_STAGES_START = os.environ['PROCESS_STAGES_START']
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

    # get LIMS data
    print("LIMS")
    sql = f"""SELECT
            a.name               AS productname,
            a.version            AS productversion,
            a.code               AS itemcode,
            a.x_product_family   AS productfamily,
            b.recd_date          AS samplerecddate,
            c.analysis,
            c.version            AS analysisversion,
            c.status,
            c.reported_name      AS testnamegeneral,
            c.batch              AS runid,
            d.lot_name           AS lotnumber,
            substr(d.lot_name,0, 8) as lotnumber_actual,
            d.x_supplier_lot     AS supplierlot,
            e.result_number,
            e.name               AS testnamedetail,
            e.entry              AS resultvalue,
            e.units              AS units,
            g.description        AS specification_description,
            g.spec_rule,
            g.max_value,
            g.min_value,
            e.status,
            e.instrument
        FROM
            lims.product a
            INNER JOIN lims.sample b ON a.name = b.product
                                        AND a.version = b.product_version
            INNER JOIN lims.test c ON b.sample_number = c.sample_number
            INNER JOIN lims.lot d ON b.lot = d.lot_number
            INNER JOIN lims.result e ON c.test_number = e.test_number
            LEFT OUTER JOIN lims.result_spec f ON f.result_number = e.result_number
            INNER JOIN lims.product_spec g ON f.product_spec_code = g.entry_code
            
        where b.recd_date > to_date('{EXTRACTION_DATE}', 'YYYY-MM-DD HH24:MI:SS')"""
    df_lims = db.lims_run_sql(sql)

    # get parameters
    print("parameters")
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
    print("process orders")
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
    print("process stages")
    sql = f"""SELECT * FROM
        (SELECT
             a.numof as process_order,
             substr(a.numlot,0,8) AS baselot,
             trim(NVL(SUBSTR(a.codeart, 0, INSTR(a.codeart, '-')-1), a.codeart))  AS trimcodeart,
             TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
             TRIM(CASE
                 WHEN(instr(a.codeart,'-') ) > 1 THEN TO_CHAR(substr(a.codeart, (instr(a.codeart,'-') + 1),length(a.codeart) ) )
                 ELSE 'FINI'
             END) AS workcentrecode
         FROM
             elan2406prd.xfp_lotstraces a
         WHERE
             fonction = 'PRODUCTION LOT'
                 AND message LIKE 'Manuf%' 
             --and a.datetrace >= '{PROCESS_STAGES_START}'
             and a.datetrace >= '20170101'
             --and a.numof = '0220982928'
         UNION
        SELECT
             a.numof as process_order,
             substr(a.numlot,0,8) AS baselot,
             trim(NVL(SUBSTR(a.codeart, 0, INSTR(a.codeart, '-')-1), a.codeart))  AS trimcodeart,
             TO_DATE(a.datetrace || a.heuretrace,'YYYYMMDDHH24MISS') AS mandecdate,
             TRIM(CASE
                 WHEN(instr(a.codeart,'-') ) > 1 THEN TO_CHAR(substr(a.codeart, (instr(a.codeart,'-') + 1),length(a.codeart) ) )
                 ELSE 'FINI'
             END) AS workcentrecode
         FROM
             arch2406prd.xfp_lotstraces a
         WHERE
             fonction = 'PRODUCTION LOT'
                 AND message LIKE 'Manuf%' 
             --and a.datetrace >= '{PROCESS_STAGES_START}'
             and a.datetrace >= '20170101'
             --and a.numof = '0220982928'
     ) PIVOT (
         MIN ( mandecdate )
     AS transdate
         FOR workcentrecode
         IN ( 'DISP',
         'G',
         'BL',
         'T',
         'CT',
         'P',
         'FINI' ))"""
    df_stages = db.xfp_run_sql(sql)
    #df_stages = df_stages.loc[df_stages["PROCESS_ORDER"].isin(df_params["PO"])]

    print("saving data")
    newest_inputdate = dt.datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S")  # get_newest_inputdate(df_params)
    db.save_key_value("braincube_last_save", newest_inputdate)
    path = PATH + "\\output\\"
    time_now = dt.datetime.today().strftime("%Y%m%d-%H%M")   
    if not os.path.exists(path):
        os.makedirs(path)    
    if not df_params.empty:
        filename_param = "\\" + "XFP_parameters-" + time_now + ".csv"
        print(path + filename_param)
        df_params.to_csv(path + filename_param, sep=';', index=False)
    if not df_orders.empty:
        filename_po = "\\" + "XFP_orders-" + time_now + ".csv"
        print(path + filename_po)
        df_orders.to_csv(path + filename_po, sep=';', index=False)
    if not df_stages.empty:
        filename_stages = "\\" + "process_stages-" + time_now + ".csv"
        print(path + filename_stages)
        df_stages.to_csv(path + filename_stages, sep=';', index=False)
    if not df_lims.empty:
        filename_lims = "\\" + "lims-" + time_now + ".csv"
        print(path + filename_lims)
        df_lims.to_csv(path + filename_lims, sep=';', index=False)

# %%
