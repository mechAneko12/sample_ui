import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_plotly_events import plotly_events
import matplotlib.pyplot as plt
import numpy as np

from plot_graph import plot_heatmap


def database_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_side_bar()
    #gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
    gb.configure_selection('single')
    gridOptions = gb.build()

    from st_aggrid.shared import GridUpdateMode
    data = AgGrid(df, 
                gridOptions=gridOptions, 
                enable_enterprise_modules=True, 
                allow_unsafe_jscode=True, 
                update_mode=GridUpdateMode.SELECTION_CHANGED)
    
    return data

def _automatic_selection(fig, raw_data):
    
    st.info('Automatic Selection')


def _range_selection(fig, raw_data):
    
    st.info('Range Selection')

def sidebar_func(fig, raw_data):
    apps = {
        '-': None,
        'Automatic Selection': _automatic_selection,
        'Range Selection': _range_selection,
    }
    selected_app_name = st.sidebar.selectbox(label='apps',
                                                options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('Please select the app')
        # st.stop()
        if fig:
            col1, col2 = st.columns(2)
            plot_heatmap(fig, selected_point=None)
            with col1:
                selected_points = plotly_events(fig)
                # print(selected_points)
                if len(selected_points) != 0:
                    st.session_state.selected_point = selected_points[0]
                    with col1:
                        len_y = raw_data.shape[1]
                        fig_y = plt.figure(figsize=(4,1))
                        plt.plot(np.arange(len_y), raw_data[selected_points[0]['y'], :])
                        st.plotly_chart(fig_y)
                    with col2:
                        len_x = raw_data.shape[0]
                        fig_x = plt.figure(figsize=(1, 4))
                        plt.plot(raw_data[:, selected_points[0]['x']], np.arange(len_x))
                        plt.gca().invert_yaxis()
                        st.plotly_chart(fig_x)

    # 選択されたアプリケーションを処理する関数を呼び出す
    else:
        if fig:
            render_func = apps[selected_app_name]
            render_func(fig, raw_data)
            

