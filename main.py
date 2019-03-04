# %%
import pandas as pd
from xfp import Xfp as xfp

# %%
#df_params_prd = pd.read_pickle("testdata/df_params_prd_pkl.zip")
#df_po_prd = pd.read_pickle("testdata/df_po_prd_pkl.zip")
#df_params_prd.loc[df_params_prd["DATATYPE"] == 2].head(500)
# df_params_prd.head(500)

# %%
df_orders = xfp.get_orders()
df_orders.head(100)
