from concurrent.futures import process
import json
import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import datetime
from pytz import timezone
import cv2
import logging

from plot_graph import plot_heatmap, plot_threeD_heatmap
from sql_process import process_get, process_post

def _data_uploader():
    st.header('Data Uploader')
    root_url = 'http://sql_app:8000'
    
    owner_id = st.selectbox('owner_id',_list_owner_id(root_url + '/users/'))
    title = st.text_input('title', '')
    url = root_url + '/users/{}/items'.format(owner_id)
    uploaded_file = st.file_uploader('File Upload', type='csv') 
    if uploaded_file is not None:
        insert_button_status = st.button(label='Insert data', on_click=_insert_button_clicked, args=(uploaded_file, title, url, ))
        if insert_button_status:
            if st.session_state.insert_status == 200:
                st.info('Succesfully inserted your data into db!')
            else:
                st.info('Error occurred! (Code: {})'.format(st.session_state.insert_status))

def _list_owner_id(url):
    r = process_get(url)
    output = []
    for _j in r.json():
        output.append(_j['id'])
    return output

def _insert_button_clicked(uploaded_file, title, url):
    uploaded_data = np.loadtxt(uploaded_file, delimiter=',')
    assert uploaded_data.dtype == np.float64
    assert uploaded_data.ndim == 2
    if title != '':
        json_data = {
            'title': title,
            'timestamp': datetime.datetime.now(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'description': uploaded_data.tolist()
        }
        r = process_post(json_data, url)
        st.session_state.insert_status = r.status_code
        if r.status_code == 200:
            logging.info('Succesfully inserted your data into db!')
            
        else:
            logging.info('Error occurred! (Code: {}, {}'.format(r.status_code, r.json()))
            

def _data_viewer(fig, raw_data):
    st.header('Data Viewer')
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

def _edge_detection(fig, raw_data):
    st.header('Edge Detection')
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
        'Data Uploader': _data_uploader,
        'Data Viewer': _data_viewer,
        'Edge Detection': _edge_detection,
        'Range Selection': _range_selection,
    }
    selected_app_name = st.sidebar.selectbox(label='apps',
                                                options=list(apps.keys()))

    if selected_app_name == '-':
        st.info('Please select the app')
        # st.stop()
        

    # 選択されたアプリケーションを処理する関数を呼び出す
    else:
        render_func = apps[selected_app_name]
        if selected_app_name == 'Data Uploader':
            render_func()
        else:
            render_func(fig, raw_data)
            
            if fig:              
                threeD_fig = plot_threeD_heatmap(raw_data.T)
                st.plotly_chart(threeD_fig, use_container_width=True)
            
def map_img(raw_data):
    data_tmp = raw_data - raw_data.min()
    data_tmp = data_tmp / data_tmp.max() * 255
    return data_tmp.astype(np.uint8)
