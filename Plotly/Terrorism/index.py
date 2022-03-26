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
            html.P("Select Region")
        ], className="create_container"),
        html.Div([
            html.P("box 2")
        ], className="create_container"),
        html.Div([
            html.P("box 3")
        ], className="create_container")
    ], id="second-container")
], id="main-container")

if __name__ == "__main__":
    app.run_server(debug=True)
