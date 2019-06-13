# DASH IMPORTS
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

# PLOTLY IMPORTS
import plotly.graph_objs as go

# OTHER IMPORTS
import numpy as np
import pandas as pd
import os

csv_files = os.listdir('energy_data/')
regions = []
for x in csv_files:
    regions.append(x.split('_')[0]) # List of regions for Dropdown menu

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div('my info',id='info',className='info'),
    html.Div('my graph',id='my-graph',className='my-graph')
])

if __name__ == '__main__':
    app.run_server(debug=True)
