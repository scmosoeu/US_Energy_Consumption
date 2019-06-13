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

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([

        dcc.Dropdown(
            id='location',
            options=[{'label':i,'value':j} for i,j in zip(regions,csv_files)],
            value=csv_files[0]
        ),

        html.Div(id='calender')

    ],className='info'),

    html.Div(id='my-graph',className='my-graph')
])

@app.callback(Output('calender','children'),
             [Input('location','value')])

def date_selector(section):
    df = pd.read_csv('energy_data/'+str(section))
    df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S')

    return dcc.DatePickerSingle(
        id='my-date-picker',
        min_date_allowed=df['Datetime'][0],
        max_date_allowed=df['Datetime'][-1],
        date=df['Datetime'][0]
    )

@app.callback(Output('my-graph','children'),
             [Input('location','value'),
              Input('my-date-picker','date')])

def my_graph(section,selected_date):
    df = pd.read_csv('/energy_data/'+str(section))
    print(df)
    data = [
        go.Bar(
            x=df[:,2],
            y=df[:,1]
        )
    ]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=['type','Bar'],
                    label='Bar Chart',
                    method='restyle'
                ),
                dict(
                    args=['type','Line'],
                    label='Line Chart',
                    method='restyle'
                )
            ]),
            showactive=True
        )
    ])

    layout = go.Layout(
        title='Energy consumption for {} region'.format(section.split('_')[0]),
        xaxis={'title':'Time of day'},
        yaxis={'title':'Energy Consumption'},
        hovermode='closest',
        updatemenus=updatemenus
    )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
