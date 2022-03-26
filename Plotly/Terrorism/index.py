import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('./modified_globalterrorismdb_0718dist.csv')

app = dash.Dash(__name__, title='terrorism')
app.layout = html.Div([

], id='main-container')
