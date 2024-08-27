#!/usr/bin/env python
# coding: utf-8

# Imports
import os
import globals
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot

# Paths
figure_path = globals.figure_path
interactive_plot_path = globals.interactive_plot_path

# Call function saveMatcher
def saveMatcher(output, 
                matcher, 
                descriptor, 
                image_num):
    # Plot BFMatcher

    # Turn interactive plotting off
    plt.ioff()

    # Create a new figure
    plt.figure()
    plt.axis('off')
    plt.imshow(output)

    # Save the figure with the image number in the filename
    plt.imsave(fname = os.path.join(figure_path,'%s-with-%s-%04d.png' % (matcher, descriptor, image_num)),
               arr = output,
               dpi = 600)

    # Close it
    plt.close()

# Function to draw an interactive 3D map of movement and rotation
def plot_movement_and_rotation(data1, data2, data3, name1='Estimation', name2='Relative Path', name3='Difference'):
    traces = []

    for j, (data, name) in enumerate(zip([data1, data2, data3], [name1, name2, name3])):
        if data is None:
            continue

        tx_values = data[:, 1]
        ty_values = data[:, 2]
        tz_values = data[:, 3]

        trace = go.Scatter3d(x=tx_values, y=ty_values, z=tz_values, mode='lines', name=name)
        traces.append(trace)

    plotly_fig = go.Figure(data=traces)

    plotly_fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ))

    plot(plotly_fig, filename = interactive_plot_path)