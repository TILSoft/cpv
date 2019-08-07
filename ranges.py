"""Extract and add XFP paramaters specs and tolerances"""
# pylint: disable=invalid-name

# %%
import os
import sys
import datetime
from bs4 import BeautifulSoup
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

        # Adding new columns
        dataframe["value_min"] = None
        dataframe["value_max"] = None
        dataframe["tolerance_min"] = None
        dataframe["tolerance_max"] = None

        try:
            # Extracting and saving (only numeric datatype)
            print(
                f"Extracting ranges - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for row in dataframe.loc[dataframe["DATATYPE"] == 1].itertuples():
                html = df_html.loc[(df_html["MANCODE"] == row.MANCODE)
                                & (df_html["BATCHID"] == row.BATCHID)
                                & (df_html["OPERATIONNUMBER"] == row.OPERATIONNUMBER),
                                "HTML"].iloc[0]
                values = cls.get_values(html, row.TAGNUMBER, row)
                dataframe.at[row.Index, "value_min"] = values[0]
                dataframe.at[row.Index, "value_max"] = values[1]
                dataframe.at[row.Index, "tolerance_min"] = values[2]
                dataframe.at[row.Index, "tolerance_max"] = values[3]
        except IndexError as e:
            print(e)
            print(row)
            raise
            sys.exit(1)
        return dataframe

    @classmethod
    def get_values(cls, html, tagid, row):
        """Extract tolerance html tags"""

        def clean(val):
            if val == "null":
                return None
            return ''.join([ch for ch in val if ch not in "[]"])

        soup = BeautifulSoup(html, 'lxml')

        try:
            param = soup.find("input", {"id": tagid})
            val_min = clean(param.get("val_min"))
            val_max = clean(param.get("val_max"))
            val_tolmin = clean(param.get("val_tolmin"))
            val_tolmax = clean(param.get("val_tolmax"))
        except (AttributeError, TypeError) as e:
            print(e)
            print(param)
            print(row)
            return (None, None, None, None)
        return (val_tolmin, val_tolmax, val_min, val_max)
