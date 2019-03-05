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
    def get_orders():
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
        df_po_arch = db.xfp_run_sql(sql_po_arch)

        df_po = pd.concat([df_po_prd,
                          df_po_arch],
                          ignore_index=True,
                          sort=False
                          ).drop_duplicates().reset_index(drop=True)
        return trim_all_columns(df_po)


    def get_tasks():
        pass

    @staticmethod
    def get_parameters(params):
        """Get parameters from XFP"""

        sql_params_prd = f"""select picode as PICODE, mancode, batchid,
                                parametercode as parametercode, inputindex,
                                inputdate, datatype,
                                numvalue, datevalue, TEXTVALUE
                                from ELAN2406PRD.e2s_pidata_man
                                where parametercode in ({params})
                                and mancode in ('0220917404', '0220936055','0220865338','0220896217','0220897771', '0220888738')
                                """
        df_prd = db.xfp_run_sql(sql_params_prd)
        # df_arch = db.xfp_run_sql(sql_po_arch)

        # df_params = pd.concat([df_prd,
        #                   df_arch],
        #                   ignore_index=True,
        #                   sort=False
        #                   ).drop_duplicates().reset_index(drop=True)
        return trim_all_columns(df_prd)