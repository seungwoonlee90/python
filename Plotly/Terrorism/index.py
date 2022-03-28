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
            html.P("Select Year"),
            dcc.RangeSlider(id='select_years',
                            min=1970,
                            max=2017,
                            step=1,
                            tooltip={"placement": "bottom",
                                     "always_visible": True},
                            dots=False,
                            marks=None,
                            value=[2010, 2017])
        ], className="create_container")
    ], id="second-container"),
    html.Div([
        html.Div([
            dcc.Graph(id='bar_chart', config={'displayModeBar': 'hover'})
        ], className="create_container two"),
        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'})
        ], className="create_container two"),

    ], id="third-container")
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


@app.callback(Output('bar_chart', 'figure'),
              [Input('w_region', 'value')],
              [Input('w_country', 'value')],
              [Input('select_years', 'value')])
def select(w_region, w_country, select_year):
    df[['nkill', 'nwound', 'attacktype1']] = df[[
        'nkill', 'nwound', 'attacktype1']].fillna(0)
    terr = df.groupby(['region_txt', 'country_txt', 'iyear'])[
        ['nkill', 'nwound', 'attacktype1']].sum().reset_index()
    terr = terr[(terr['region_txt'] == w_region) & (terr['country_txt'] == w_country) & (
        terr['iyear'] >= select_year[0]) & (terr['iyear'] <= select_year[1])]
    return {
        'data': [go.Scatter(
            x=terr['iyear'],
            y=terr['nkill'],
            name='Death',
            mode='markers+lines',
            line=dict(shape='spline', smoothing=1, width=3, color='#FF00FF'),
            marker=dict(color='white', size=10, symbol='circle',
                        line=dict(color='#FF00FF', width=2)),
            hoverinfo='text',
            hovertext='<b>Region<b/> : ' + terr['region_txt'] + '<br />' +
            '<b>kill<b/> : ' + [f'{x:,.0f}' for x in terr['nkill']]
        ),

            go.Bar(
            x=terr['iyear'],
            y=terr['nwound'],
            text=terr['nwound'],
            texttemplate='%{text:,.0f}',
            textposition='auto',
            name='Injured',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext='<b>Region<b/> : ' + terr['region_txt'] + '<br />' +
            '<b>Injured<b/> : ' + [f'{x:,.0f}' for x in terr['nwound']]
        ),
            go.Bar(
            x=terr['iyear'],
            y=terr['attacktype1'],
            text=terr['attacktype1'],
            texttemplate='%{text:,.0f}',
            textposition='auto',
            name='Attack',
            marker=dict(color='red'),
            hoverinfo='text',
            hovertext='<b>Region<b/> : ' + terr['region_txt'] + '<br />' +
            '<b>Attack<b/> : ' + [f'{x:,.0f}' for x in terr['attacktype1']]
        )],
        'layout': go.Layout(
            title={'text': 'death_' + (w_region) + '_' + (w_country)},
            paper_bgcolor='#010915',
            plot_bgcolor='#010915',
            font=dict(color='white'),
            xaxis=dict(showline=True, showgrid=True,
                       linecolor='white', dtick=1),
            yaxis=dict(showline=True, showgrid=True,
                       linecolor='white'),
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
