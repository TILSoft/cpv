"""Extract and add XFP paramaters specs and tolerances"""
# pylint: disable=invalid-name

# %%
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from helpers import create_sql_snippet, is_string_digit
from xfp import Xfp as xfp


# %%
class Ranges:
    """Extract and add XFP paramaters specs and tolerances"""

    @classmethod
    def params_to_values(cls, df_main, redo):
        """Extracts parameters and saves actual values"""

        # get all spec parameters values
        df_values = pd.concat([
            df_main.loc[df_main["value_min"].notna(), ["MANCODE", "BATCHID",
                                                    "value_min"]].rename(columns={"value_min": "value"}),
            df_main.loc[df_main["value_max"].notna(), ["MANCODE", "BATCHID",
                                                    "value_max"]].rename(columns={"value_max": "value"}),
            df_main.loc[df_main["tolerance_min"].notna(), ["MANCODE", "BATCHID",
                                                    "tolerance_min"]].rename(columns={"tolerance_min": "value"}),
            df_main.loc[df_main["tolerance_max"].notna(), ["MANCODE", "BATCHID",
                                                    "tolerance_max"]].rename(columns={"tolerance_max": "value"})],
            sort=False).drop_duplicates()

        # drop all but parameter names
        df_values.dropna(subset=["value"], inplace=True)
        df_values = df_values.loc[~df_values["value"].apply(is_string_digit)]

        # query xfp db
        df_values = xfp.get_parameters(redo=redo, df=df_values)

        # take only parameters values entered last in the given batchid
        df_values = df_values.loc[df_values.groupby(
            ["MANCODE", "BATCHID", "PARAMETERCODE"])["INPUTINDEX"].idxmax()]

        try:
            # go thrugh each spec parameter and replace it with an actual value
            for row in df_main.itertuples():
                for col in ["value_min", "value_max", "tolerance_min", "tolerance_max"]:
                    spec_param = df_main.at[row.Index, col]
                    if (spec_param is not None) and (not is_string_digit(spec_param)):
                        temp = df_values.loc[(
                            df_values["MANCODE"] == row.MANCODE)]
                        value = df_values.loc[(df_values["MANCODE"] == row.MANCODE)
                                            & (df_values["BATCHID"] == row.BATCHID)
                                            & (df_values["PARAMETERCODE"] == spec_param),
                                            "VALUE"].iloc[0]
                        df_main.at[row.Index, col] = value
        except IndexError as e:
            print(e)
            print(row)
            print("spec_param = " + spec_param)
            print("col = " + col)
            print(temp)
            raise
        return df_main


    @classmethod
    def add_ranges(cls, dataframe, arch_db):
        """Append columns with limits and tolerances"""

        sql_text = create_sql_snippet(
            "where", ["codefab", "batchid", "numoperation", "inputindex"],
            dataframe.loc[:, ["MANCODE", "BATCHID", "OPERATIONNUMBER", "BROWSINGINDEX"]].drop_duplicates())

        df_html = xfp.get_html(sql_text, arch_db)

        # Adding new columns
        dataframe["value_min"] = None
        dataframe["value_max"] = None
        dataframe["tolerance_min"] = None
        dataframe["tolerance_max"] = None

        try:
            # Extracting and saving (only numeric datatype)
            for row in dataframe.loc[dataframe["DATATYPE"] == 1].itertuples():
                html = df_html.loc[(df_html["MANCODE"] == row.MANCODE)
                                & (df_html["BATCHID"] == row.BATCHID)
                                & (df_html["OPERATIONNUMBER"] == row.OPERATIONNUMBER)
                                & (df_html["INPUTINDEX"] == row.BROWSINGINDEX),
                                "HTML"].iloc[0]

                # it is null for tasks in progress
                if not html:
                    html = xfp.get_html_cmdtext(row)

                values = cls.get_values(html, row.TAGNUMBER, row)
                dataframe.at[row.Index, "value_min"] = values[0]
                dataframe.at[row.Index, "value_max"] = values[1]
                dataframe.at[row.Index, "tolerance_min"] = values[2]
                dataframe.at[row.Index, "tolerance_max"] = values[3]
        except IndexError as e:
            print(e)
            print(row)
            raise

        dataframe = cls.params_to_values(dataframe, arch_db)
        return dataframe

    @classmethod
    def get_values(cls, html, tagid, row):
        """Extract tolerance html tags"""

        def clean(val):
            if val == "null":
                return None
            return ''.join([ch for ch in val if ch not in "[]"])

        try:
            soup = BeautifulSoup(html, 'lxml')
        except TypeError as e:
            print(e)
            print(row)
            raise

        try:
            param = soup.find("input", {"id": tagid})
            val_min = clean(param.get("val_min"))
            val_max = clean(param.get("val_max"))
            val_tolmin = clean(param.get("val_tolmin"))
            val_tolmax = clean(param.get("val_tolmax"))
        # do not exit just return nulls
        except (AttributeError, TypeError) as e:
            print(e)
            print(param)
            print(row)
            return (None, None, None, None)
        return (val_tolmin, val_tolmax, val_min, val_max)
