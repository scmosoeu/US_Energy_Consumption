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
from datetime import datetime
import os

csv_files = os.listdir('energy_data/')
regions = []
for x in csv_files:
    regions.append(x.split('_')[0]) # List of regions for Dropdown menu

global df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='location',
                options=[{'label':i,'value':j} for i,j in zip(regions,csv_files)],
                value=csv_files[0]
            )
        ],style={'width':'40%','display':'inline-block','paddingRight':'30px'}),

        html.H4('Select date:',
            style={'display':'inline-block','lineHeight':'0px'}),

        html.Div(id='calender',
            style={
                'width':'40%',
                'display':'inline-block',
                'verticalAlign':'top',
                'paddingLeft':'10px'
            }
        )
    ]),

    html.Div(id='my-graph',style={'paddingTop':'30px'})
])

@app.callback(Output('calender','children'),
             [Input('location','value')])

def date_selector(section):

    df = pd.read_csv('energy_data/'+str(section))
    df['Date'] = df['Datetime'].apply(lambda x: x.split(' ')[0])
    return dcc.DatePickerSingle(
        id='my-date-picker',
        display_format='D/M/Y',
        min_date_allowed=df['Date'].iloc[0],
        max_date_allowed=df['Date'].iloc[-1],
        date=df['Date'].iloc[0]
    )

@app.callback(Output('my-graph','children'),
             [Input('my-date-picker','value')])

def my_graph(selected_date):

    df['Date'] = df['Datetime'].apply(lambda x: x.split(' ')[0])
    df['Time'] = df['Datetime'].apply(lambda x: x.split(' ')[1])

    df = df[df['Date'] == selected_date.split(' ')[0]]

    data = [
        go.Bar(
            x=df['Time'],
            y=df[str(section.split('_')[0])+'_MW']
        )
    ]

    layout = go.Layout(
        hovermode='closest',
        title='Energy consumption for {} region'.format(section.split('_')[0]),
        xaxis={'title':'Time of day'},
        yaxis={'title':'Energy consumption (MW)'},
        height=750
    )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
