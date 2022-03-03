import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json

from sidebar_app import sidebar_func
from sql_process import database_table, process_get, process_post
from plot_graph import plot_threeD_heatmap

import warnings
warnings.simplefilter('ignore', FutureWarning)

backend_url = 'http://127.0.0.1:8000'

if 'selected_point' not in st.session_state: 
    st.session_state.selected_point = None

st.set_page_config(page_title='OFC data tool', layout="wide") 
st.title('Optical Frequency Comb data viewer')

sql_items = process_get(backend_url + '/items/')
sql_items_df = pd.DataFrame.from_dict(sql_items)

data = database_table(sql_items_df.reindex(columns=['id', 'title', 'owner_id', 'description']))

selected_rows = data["selected_rows"]
selected_rows = pd.DataFrame(selected_rows)

# _selected_row = None
fig = None
raw_data = None
if len(selected_rows) != 0:
    # print(selected_rows)
    post_content = {'id': int(selected_rows.loc[0, 'id'])}
    _selected_row = process_post(json.dumps(post_content),
                                 server_url=backend_url + '/item_by_id/')
    fig = px.imshow(_selected_row['description'])
    raw_data = np.array(_selected_row['description'])

sidebar_func(fig, raw_data)

if fig:              
    threeD_fig = plot_threeD_heatmap(raw_data.T)
    st.plotly_chart(threeD_fig, use_container_width=True)
    