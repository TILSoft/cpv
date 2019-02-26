# %%
import pandas as pd

# %%
df_params_prd = pd.read_pickle("testdata/df_params_prd_pkl.zip")
df_po_prd = pd.read_pickle("testdata/df_po_prd_pkl.zip")
df_params_prd.loc[df_params_prd["DATATYPE"] == 2].head(500)
# df_params_prd.head(500)

# %%
df_po_prd.head()
