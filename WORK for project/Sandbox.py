# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
import pandas as pd
from IPython.display import display

df = pd.read_csv("openfoodfacts_search2.csv", keep_default_na = False, sep = ';', header = 0)
pd.options.display.max_columns = None

html_str = df.head(60).to_html()

Html_file = open("extracted_search.html","w",encoding="utf-8")
Html_file.write(html_str)
Html_file.close()


#%%



