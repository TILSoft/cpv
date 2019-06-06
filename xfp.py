"""Select queries on the XFP database"""
# %%
import os
import pandas as pd
from database import DataBase as db
from myhelpers import trim_all_columns

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
                        --and o.numof in ('0220865338', '0220886360')
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
            df_po = pd.concat([df_po_prd,
                              df_po_arch],
                              ignore_index=True,
                              sort=False
                              ).drop_duplicates().reset_index(drop=True)
        else:
            df_po = df_po_prd.drop_duplicates().reset_index(drop=True)

        return trim_all_columns(df_po)


    @staticmethod
    def get_parameters(params, time, redo=False, arch_db=True):
        """Get parameters from XFP"""

        date_txt = f"""and inputdate >= TO_DATE('{time}', 'yyyy-mm-dd hh24:mi:ss')"""
        if redo:
            date_txt = ""

        sql_params_prd = f"""select picode as picode, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, datatype,
                                numvalue, datevalue,
                                dbms_lob.substr(textvalue,4000,1) as textvalue
                                from ELAN2406PRD.e2s_pidata_man
                                where parametercode in ({params})
                                --and mancode in ('0220917404', '0220936055','0220865338','0220896217','0220897771', '0220888738')
                                --and mancode in ('0220917404')
                                {date_txt}
                                """

        sql_params_arch = f"""select picode as picode, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, datatype,
                                numvalue, datevalue,
                                dbms_lob.substr(textvalue,4000,1) as textvalue
                                from arch2406PRD.e2s_pidata_man
                                where parametercode in ({params})
                                --and mancode in ('0220917404', '0220936055','0220865338','0220896217','0220897771', '0220888738')
                                --and mancode in ('0220917404')
                                {date_txt}
                                """
        df_prd = db.xfp_run_sql(sql_params_prd)

        if arch_db:
            df_arch = db.xfp_run_sql(sql_params_arch)
            df_params = pd.concat([df_prd,
                                  df_arch],
                                  ignore_index=True,
                                  sort=False
                                  ).drop_duplicates().reset_index(drop=True)
        else:
            df_params = df_prd.drop_duplicates().reset_index(drop=True)

        # the dt.strftime cant handle when the date is too old or too new
        df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) & (df_params["DATEVALUE"].astype(str).str.startswith("0"))].index
               ,inplace=True
               ,axis=0)
        df_params.drop(df_params.loc[(df_params["DATATYPE"] == 2) & (df_params["DATEVALUE"].astype(str).str.startswith("28"))].index
               ,inplace=True
               ,axis=0)

        # check and save an actual value
        df_params["VALUE"] = df_params["NUMVALUE"]
        df_params.loc[df_params["DATATYPE"] == 0, "VALUE"] = df_params["TEXTVALUE"]
        df_params.loc[df_params["DATATYPE"] == 2, "VALUE"] = df_params["DATEVALUE"].dt.strftime('%d-%m-%Y %H:%M:%S')

        # drop Null values
        df_params.drop(df_params.loc[df_params["VALUE"].isnull()].index, inplace=True, axis=0)

        return trim_all_columns(df_params)



    @staticmethod
    def get_newest_inputdate(df):
        return df.loc[:, "INPUTDATE"].max()


    @staticmethod
    def get_tasks(df):
        pass