import numpy as np
import plotly.graph_objects as go

def plot_heatmap(fig, selected_point=None):
    if selected_point:
        fig_tmp_1 = go.Scatter(x=[selected_point['x'],selected_point['x']],
                                y=[5,95],
                                mode='lines',
                                line=go.scatter.Line(color='white'),
                                showlegend=False)
        fig_tmp_2 = go.Scatter(x=[0,100],
                                y=[selected_point['y'],selected_point['y']],
                                mode='lines',
                                line=go.scatter.Line(color='white'),
                                showlegend=False)
        fig.add_trace(fig_tmp_1); fig.add_trace(fig_tmp_2)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showspikes=True, spikemode='across')
    fig.update_yaxes(showspikes=True, spikemode='across')
    
    return fig

def plot_threeD_heatmap(data):
    threeD_fig = go.Figure(go.Surface(
    contours = {
        'x': {'show': True},
        'z': {'show': True}
    },
    x = np.arange(len(data[0])),
    y = np.arange(len(data)),
    z = data))
    
    threeD_fig.update_layout(
        scene = {
            #'xaxis': {'nticks': 20},
            #'zaxis': {'nticks': 4},
            'camera_eye': {'x': 1, 'y': 0, 'z': 1},
            #'aspectratio': {'x': 1, 'y': 1, 'z': 0.2}
        })
    return threeD_fig