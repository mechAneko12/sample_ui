from concurrent.futures import process
import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import cv2

from plot_graph import plot_heatmap

def _automatic_selection(fig, raw_data):
    st.header('Automatic Selection')
    if fig:
        slider_thre1 = st.slider('threshold 1', 0, 1000, 200, 25)
        slider_thre2 = st.slider('threshold 2', 0, 1000, 450, 25)
        col1, col2 = st.columns(2)
        
        # binarization and edge detection
        processed_img = map_img(raw_data)
        mask = cv2.Canny(processed_img, slider_thre1, slider_thre2) 
        # selected_point = something
        
        plot_heatmap(fig, selected_point=None)
        with col1:
            st.plotly_chart(fig)
                
        with col2:
            fig_edge = px.imshow(mask, width=450, height=450)
            fig_edge.update_layout(coloraxis_showscale=False)
            # plt.subplots_adjust(left=5, right=10, bottom=5, top=10)
            st.plotly_chart(fig_edge)
            


def _range_selection(fig, raw_data):
    st.header('Range Selection')

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
        render_func = apps[selected_app_name]
        render_func(fig, raw_data)
            
def map_img(raw_data):
    data_tmp = raw_data - raw_data.min()
    data_tmp = data_tmp / data_tmp.max() * 255
    return data_tmp.astype(np.uint8)
