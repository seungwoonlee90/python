import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('./modified_globalterrorismdb_0718dist.csv')

app = dash.Dash(__name__, title="terrorism")
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3('Global Terrorism Database'),
                html.H5('1970 - 2017')
            ])
        ], id="title")
    ], id="header"),
    html.Div([
        html.Div([
            html.P("Select Region"),
            dcc.Dropdown(id='w_region',
                         multi=False,
                         searchable=True,
                         value='East Asia',
                         placeholder='Select Region',
                         options=[{'label': c, 'value': c} for c in (df['region_txt'].unique())], className="dropdown")
        ], className="create_container"),
        html.Div([
            html.P("Select Country"),
            dcc.Dropdown(id='w_country',
                         multi=False,
                         searchable=True,
                         placeholder='Select Country',
                         options=[], className="dropdown")
        ], className="create_container"),
        html.Div([
            html.P("box 3")
        ], className="create_container")
    ], id="second-container")
], id="main-container")


@app.callback(Output('w_country', 'options'),
              [Input('w_region', 'value')])
def select(w_region):
    terr = df[df['region_txt'] == w_region]
    return [{'label': i, 'value': i} for i in terr['country_txt'].unique()]


@app.callback(Output('w_country', 'value'),
              [Input('w_country', 'options')])
def select(w_country):
    return [k['value'] for k in w_country][0]


if __name__ == "__main__":
    app.run_server(debug=True)
