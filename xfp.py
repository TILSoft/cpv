"""Select queries on the XFP database"""
# %%
import pandas as pd
import datetime
from database import DataBase as db
from helpers import trim_all_columns, create_sql_snippet, create_sql_list

# %%
class Xfp:
    """Select queries on the XFP database"""

    @staticmethod
    def get_html_cmdtext(row):
        """
        For EMI tasks the html is saved to e2s_pitext_man only after task is completed
        so for tasks in progress there is a need no extract spec values from the e2s_pidata_man
        able. Note it can't be done for all as cmdtext column may be null once task is completed.
        As this is only for in porogress task no need to query the archive db.
        """
        sql = f"""select cmdtext from elan2406prd.e2s_pidata_man where
                    mancode = '{row.MANCODE}'
                    and batchid = '{row.BATCHID}'
                    and parametercode = '{row.PARAMETERCODE}'
                    and inputindex = '{row.INPUTINDEX}'
                    and operationnumber = '{row.OPERATIONNUMBER}'
                    and browsingindex = '{row.BROWSINGINDEX}'
            """
        try:
            return db.xfp_run_sql(sql).iat[0, 0]
        except IndexError as e:
            print("Inside of get_html_cmdtext")
            print(e)
            print(row)
            print("\n")
            return None


    @staticmethod
    def get_html(sql_text, arch_db):
        """Extracts content of EMI tasks to use to extract parameters ranges"""
        sql_prd = f"""select codefab as mancode, batchid,
                        numoperation as OPERATIONNUMBER,
                        inputindex,
                        texte as html
                        from elan2406prd.e2s_pitext_man
                        {sql_text}"""
        df_prd = db.xfp_run_sql(sql_prd)
        if arch_db:
            sql_arch = f"""select codefab as mancode, batchid,
                numoperation as OPERATIONNUMBER,
                inputindex,
                texte as html
                from arch2406prd.e2s_pitext_man
                {sql_text}"""
            df_arch = db.xfp_run_sql(sql_arch)
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
    def get_parameters(redo, time=None, params=None, orders=None, df=None):
        """Get parameters from XFP"""

        # if there is df there realy should be no orders or params
        sql_text = ""
        if df is not None:
            sql_text = create_sql_snippet("and", ["mancode", "batchid", "parametercode"], df)
        else:
            if orders:
                orders = create_sql_list("and", "mancode", orders)
                sql_text += orders
            if params:
                params = create_sql_list("and", "parametercode", params)
                sql_text += params

        if time:
            time = f"""and inputdate >= TO_DATE('{time}',
                      'yyyy-mm-dd hh24:mi:ss')"""
        else:
            time = ""

        def get_string(db, sql_text, time):
            return f"""select picode as picode, mancode, batchid,
                            parametercode as parametercode, inputindex,
                            inputdate, operationnumber, tagnumber, datatype,
                            numvalue, datevalue,
                            textvalue as textvalue,
                            browsingindex
                            from {db}.e2s_pidata_man
                            where tagnumber <> 0 --filter out output parameters
                            and forced = 0
                            {sql_text}
                            {time}"""

        sql_string = get_string("ELAN2406PRD", sql_text, time)
        df_prd = db.xfp_run_sql(sql_string)

        if redo:
            sql_string = get_string("ARCH2406PRD", sql_text, time)
            df_arch = db.xfp_run_sql(sql_string)
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
        orders = create_sql_list("and", "mancode", orders)
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
