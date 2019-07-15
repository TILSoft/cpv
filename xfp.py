"""Select queries on the XFP database"""
# %%
import pandas as pd
from database import DataBase as db
from helpers import trim_all_columns
from helpers import create_sql_snippet

# %%


class Xfp:
    """Select queries on the XFP database"""

    @staticmethod
    def get_orders(arch_db=True):
        """Get work orders from XFP"""

        sql_po_prd = """select o.numof as po, o.codeproduit as material,
                        o.numlotpharma as batch,
                        o.designationproduit as description,
                        o.dtdatecreaparsyst as po_launchdate,
                        o.codemo as emi_master
                        from ELAN2406PRD.xfp_ofentete o
                        where o.indiceof = 0 and o.etat in ('F', 'S', 'E')
                        """
        sql_po_arch = """select o.numof as po, o.codeproduit as material,
                        o.numlotpharma as batch,
                        o.designationproduit as description,
                        o.dtdatecreaparsyst as po_launchdate,
                        o.codemo as emi_master
                        from arch2406PRD.xfp_ofentete o
                        where o.indiceof = 0 and o.etat in ('F', 'S', 'E')
                        """

        df_po_prd = db.xfp_run_sql(sql_po_prd)

        if arch_db:
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

        special = False
        orders = ""
        date_txt = f"""and inputdate >= TO_DATE('{time}',
                      'yyyy-mm-dd hh24:mi:ss')"""
        params = create_sql_snippet("where", "parametercode", params)

        if wos:
            special = True
            orders = create_sql_snippet("and", "mancode", wos)
        if redo or special:
            date_txt = ""

        sql_params_prd = f"""select picode as picode, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, operationnumber, datatype,
                                numvalue, datevalue,
                                dbms_lob.substr(textvalue,4000,1) as textvalue
                                from ELAN2406PRD.e2s_pidata_man
                                {params}
                                {orders}
                                {date_txt}
                                """

        sql_params_arch = f"""select picode as picode, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, operationnumber, datatype,
                                numvalue, datevalue,
                                dbms_lob.substr(textvalue,4000,1) as textvalue
                                from arch2406PRD.e2s_pidata_man
                                {params}
                                {date_txt}
                                """
        df_prd = db.xfp_run_sql(sql_params_prd)

        if arch_db:
            df_arch = db.xfp_run_sql(sql_params_arch)
            df_params = pd.concat([df_prd, df_arch],
                                  ignore_index=True,
                                  sort=False) \
                .drop_duplicates().reset_index(drop=True)
        else:
            df_params = df_prd.drop_duplicates().reset_index(drop=True)

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
    def get_newest_inputdate(dataframe):
        """Finds the newest date parameter index was created"""
        return dataframe.loc[:, "INPUTDATE"].max()

    @staticmethod
    def get_tasks(orders, arch_db):
        """Extracts list of EMI tasks to be used in merging with special parameters"""
        orders = create_sql_snippet("and", "mancode", orders)
        sql_prd = f"""select mancode, manindex, taskid, batchid, elementid,
                    pfccode, title from elan2406prd.e2s_pfc_task_man
                        where status <> 6
                        {orders}"""
        sql_arch = f"""select mancode, manindex, taskid, batchid, elementid,
                    pfccode, title from elan2406prd.e2s_pfc_task_man
                        where status <> 6
                        {orders}"""
        df_prd = db.xfp_run_sql(sql_prd)
        if arch_db:
            df_arch = db.xfp_run_sql(sql_arch)
            df_tasks = pd.concat([df_prd, df_arch],
                                 ignore_index=True,
                                 sort=False) \
                .drop_duplicates().reset_index(drop=True)
        else:
            df_tasks = df_prd.drop_duplicates().reset_index(drop=True)
        return df_tasks
