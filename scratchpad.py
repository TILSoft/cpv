# %%
import pandas as pd

# %%
def create_sql_snippet_html(df):
        """Create sql text"""

        # # only get EMI html if CMDTEXT is empty
        # df = df.loc[df["CMDTEXT"].isnull(),  ["MANCODE", "BATCHID",
        #                 "OPERATIONNUMBER"]].drop_duplicates()

        txt = ""
        for row in df.itertuples():
            print(row)
            txt += (f"or (codefab = '{row.MANCODE}' "
                    f"and batchid = '{row.BATCHID}' "
                    f"and numoperation = '{row.OPERATIONNUMBER}' "
                    f"and inputindex = '{row.BROWSINGINDEX}')\n ")
        return "(" + txt[3:-1] + ")"


create_sql_snippet_html(df_param_special)


#%%
