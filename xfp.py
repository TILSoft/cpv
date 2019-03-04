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
    def get_parameters():
        pass
