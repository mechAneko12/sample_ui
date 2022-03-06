import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from PIL import Image

from sidebar_app import sidebar_func
from sql_process import database_table, process_get, process_post

import warnings
warnings.simplefilter('ignore', FutureWarning)

# backend_url = 'http://127.0.0.1:8000'
backend_url = 'http://sql_app:8000'

if 'selected_point' not in st.session_state: 
    st.session_state.selected_point = None

im = Image.open('icon_2.png')
st.set_page_config(page_title='OFC data tool', page_icon=im, layout='wide') 
st.title('Optical Frequency Comb data viewer')

sql_items = process_get(backend_url + '/items/').json()
sql_items_df = pd.DataFrame.from_dict(sql_items)

data = database_table(sql_items_df.reindex(columns=['id', 'timestamp', 'title', 'owner_id', 'description']))

selected_rows = data['selected_rows']
selected_rows = pd.DataFrame(selected_rows)

# _selected_row = None
fig = None
raw_data = None
if len(selected_rows) != 0:
    # print(selected_rows)
    post_content = {'id': int(selected_rows.loc[0, 'id'])}
    _selected_row = process_post(post_content,
                                 server_url=backend_url + '/item_by_id/').json()
    raw_data = np.array(_selected_row['description'])
    fig = px.imshow(raw_data, width=450, height=450)

sidebar_func(fig, raw_data)
    