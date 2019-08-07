"""Select queries on the XFP database"""
# %%
import pandas as pd
import datetime
from database import DataBase as db
from helpers import trim_all_columns
from helpers import create_sql_snippet

# %%
class Xfp:
    """Select queries on the XFP database"""

    @staticmethod
    def get_html(sql_text, arch_db):
        """Extracts content of EMI tasks to use to extract parameters ranges"""
        print("Extracting html from PROD")
        sql_prd = f"""select codefab as mancode, batchid,
                        numoperation as OPERATIONNUMBER,
                        texte as html
                        from elan2406prd.e2s_pitext_man
                        where {sql_text}"""
        df_prd = db.xfp_run_sql(sql_prd)
        if arch_db:
            print(f"Extracting html from ARCHIVE - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            sql_arch = f"""select codefab as mancode, batchid,
                numoperation as OPERATIONNUMBER,
                texte as html
                from arch2406prd.e2s_pitext_man
                where {sql_text}"""
            df_arch = db.xfp_run_sql(sql_arch)
            print(f"Joining html PROOD and ARCHIVE - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            df_tasks = pd.concat([df_prd, df_arch],
                                ignore_index=True,
                                sort=False) \
                .drop_duplicates().reset_index(drop=True)
        else:
            df_tasks = df_prd.drop_duplicates().reset_index(drop=True)
        return df_tasks


    @staticmethod
    def get_orders(arch_db=True):
        """Get work orders from XFP"""

        sql_po_prd = """select o.numof as po, o.codeproduit as material,
                        o.numlotpharma as batch,
                        o.designationproduit as description,
                        o.dtdatecreaparsyst as po_launchdate,
                        o.codemo as emi_master,
                        o.quantiteof as order_qty,
                        o.uniteof as unit
                        from ELAN2406PRD.xfp_ofentete o
                        where o.indiceof = 0 and o.etat in ('F', 'S', 'E')
                        """

        df_po_prd = db.xfp_run_sql(sql_po_prd)

        if arch_db:
            sql_po_arch = """select o.numof as po, o.codeproduit as material,
                o.numlotpharma as batch,
                o.designationproduit as description,
                o.dtdatecreaparsyst as po_launchdate,
                o.codemo as emi_master,
                o.quantiteof as order_qty,
                o.uniteof as unit
                from arch2406PRD.xfp_ofentete o
                where o.indiceof = 0 and o.etat in ('F', 'S', 'E')
                """
            df_po_arch = db.xfp_run_sql(sql_po_arch)
            df_po = pd.concat([df_po_prd, df_po_arch],
                              ignore_index=True,
                              sort=False).drop_duplicates().reset_index(drop=True)
        else:
            df_po = df_po_prd.drop_duplicates().reset_index(drop=True)

        return trim_all_columns(df_po)

    @staticmethod
    def get_parameters(params, wos, time, redo, arch_db):
        """Get parameters from XFP"""

        orders = ""
        date_txt = f"""and inputdate >= TO_DATE('{time}',
                      'yyyy-mm-dd hh24:mi:ss')"""
        params = create_sql_snippet("and", "parametercode", params)

        if wos:
            orders = create_sql_snippet("and", "mancode", wos)
        if redo:
            date_txt = ""
        sql_params_prd = f"""select picode as picode, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, operationnumber, tagnumber, datatype,
                                numvalue, datevalue,
                                textvalue as textvalue
                                from ELAN2406PRD.e2s_pidata_man
                                where tagnumber <> 0 --filter out output parameters
                                {params}
                                {orders}
                                {date_txt}
                                """
        df_prd = db.xfp_run_sql(sql_params_prd)

        if arch_db:
            sql_params_arch = f"""select picode as picode, mancode, batchid,
                        parametercode as parametercode, inputindex,
                        inputdate, operationnumber, tagnumber, datatype,
                        numvalue, datevalue,
                        textvalue as textvalue
                        from arch2406PRD.e2s_pidata_man
                        where tagnumber <> 0 --filter out output parameters
                        {params}
                        {date_txt}
                        """
            df_arch = db.xfp_run_sql(sql_params_arch)
            df_params = pd.concat([df_prd, df_arch],
                                  ignore_index=True,
                                  sort=False) \
                .drop_duplicates().reset_index(drop=True)
        else:
            df_params = df_prd.drop_duplicates().reset_index(drop=True)

        # Exit early if df is empty
        if df_params.empty:
            return df_params

        # for some reason there are some strange dates in the database
        df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                     (df_params["DATEVALUE"]
                                      .astype(str).str.startswith("0"))].index,
                       inplace=True, axis=0)
        df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                     (df_params["DATEVALUE"]
                                      .astype(str).str.startswith("28"))].index,
                       inplace=True, axis=0)
        df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) &
                                     (df_params["DATEVALUE"]
                                      .astype(str).str.startswith("1900"))].index,
                       inplace=True, axis=0)

        # Rounding
        df_params["NUMVALUE"] = df_params["NUMVALUE"].round(2)
        # check and save an actual value
        df_params["VALUE"] = df_params["NUMVALUE"]
        df_params.loc[df_params["DATATYPE"] == 0, "VALUE"] = \
            df_params["TEXTVALUE"]
        df_params.loc[df_params["DATATYPE"] == 2, "VALUE"] = \
            df_params["DATEVALUE"].dt.strftime('%d-%m-%Y %H:%M:%S')

        # drop Null values
        df_params.drop(df_params.loc[df_params["VALUE"].isnull()]
                       .index, inplace=True, axis=0)

        return trim_all_columns(df_params)

    @staticmethod
    def get_tasks(orders, arch_db):
        """Extracts list of EMI tasks to be used in merging with special parameters"""
        orders = create_sql_snippet("and", "mancode", orders)
        sql_prd = f"""select mancode, manindex, taskid, batchid, elementid,
                    pfccode, title from elan2406prd.e2s_pfc_task_man
                        where status <> 6
                        {orders}"""
        df_prd = db.xfp_run_sql(sql_prd)
        if arch_db:
            sql_arch = f"""select mancode, manindex, taskid, batchid, elementid,
            pfccode, title from arch2406prd.e2s_pfc_task_man
                where status <> 6
                {orders}"""
            df_arch = db.xfp_run_sql(sql_arch)
            df_tasks = pd.concat([df_prd, df_arch],
                                 ignore_index=True,
                                 sort=False) \
                .drop_duplicates().reset_index(drop=True)
        else:
            df_tasks = df_prd.drop_duplicates().reset_index(drop=True)
        return df_tasks
