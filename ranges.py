"""Extract and add XFP paramaters specs and tolerances"""
# pylint: disable=invalid-name

# %%
import os
import pandas as pd
from xfp import Xfp as xfp

# %%
class Ranges:
    """Extract and add XFP paramaters specs and tolerances"""

    __DB = os.environ['MYSQL_DB']

    @classmethod
    def create_sql_snippet_html(cls, df):
        """Create sql text"""
        df = df.loc[:, ["MANCODE", "BATCHID",
                        "OPERATIONNUMBER"]].drop_duplicates()
        txt = ""
        for row in df.itertuples():
            txt += (f"or (codefab = '{row.MANCODE}' "
                    f"and batchid = '{row.BATCHID}' "
                    f"and numoperation = '{row.OPERATIONNUMBER}')\n")
        return "(" + txt[3:-1] + ")"

    @classmethod
    def add_ranges(cls, dataframe, arch_db):
        """Append 2 columns with limits and 2 with tolerances"""

        sql_text = cls.create_sql_snippet_html(dataframe)
        df_html = xfp.get_html(sql_text, arch_db)

