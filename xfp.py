"""Select queries on the XFP database"""
# %%
import os
import pandas as pd
from database import DataBase as db

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
                        o.codemo as emi_master,
                        o.indicemo as emi_master_rev
                        from ELAN2406PRD.xfp_ofentete o
                        where o.indiceof = 0 and o.etat in ('F', 'S', 'E')
                        --and o.numof in ('0220865338', '0220886360')"""

        df_po_prd = db.xfp_run_sql(sql_po_prd)
        # df_pr_arch = db.xfp_run_sql(sql_po_arch)
        return df_po_prd

    def get_tasks():
        pass

    def get_parameters():
        pass
