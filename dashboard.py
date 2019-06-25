# DASH IMPORTS
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

server = app.server

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='location',
                options=[{'label':i,'value':j} for i,j in zip(regions,csv_files)],
                value=csv_files[0]
            )
        ],style={'width':'30%','display':'inline-block','paddingRight':'30px'}),

        html.Div('Select date:',
            style={
                'display':'inline-block',
                'fontWeight':'bold',
                'fontSize':18
            }),

        html.Div(id='calender',
            style={
                'width':'50%',
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
             [Input('my-date-picker','date')],
             [State('location','value')])

def my_graph(selected_date,section):

    df = pd.read_csv('energy_data/'+str(section))
    df['Date'] = df['Datetime'].apply(lambda x: x.split(' ')[0])
    df['Time'] = df['Datetime'].apply(lambda x: x.split(' ')[1])
    df['Time'] = df['Time'].apply(lambda x: x[0:5]) # removing the milliseconds
    df = df[df['Date'] == selected_date.split(' ')[0]]

    data = [
        go.Bar(
            x=df['Time'],
            y=df[str(section.split('_')[0])+'_MW'],
            name='Energy Consumption'
        ),
        go.Scatter(
            x=df['Time'],
            y=[df[str(section.split('_')[0])+'_MW'].mean()]*len(df['Time']),
            name='Average Energy Consumption',
            line={'color':'red','dash':'dash'}
        )
    ]

    layout = go.Layout(
        hovermode='closest',
        title='Energy consumption for {} region'.format(section.split('_')[0]),
        xaxis={'title':'Time of day'},
        yaxis={'title':'Energy consumption (MW)'},
        font={'size':14},
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
