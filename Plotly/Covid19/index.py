import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

#unpivot the data
def data_unpivot(url, value_name) :
    df = pd.read_csv(url)
    date = df.columns[4:]
    total = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                    value_vars=date, var_name = 'date', value_name = value_name)
    return total
confirmed = data_unpivot(url_confirmed, 'confirmed')
deaths = data_unpivot(url_deaths, 'death')
recovered = data_unpivot(url_recovered, 'recovered')

#merging data frames
covid_data = confirmed.merge(deaths, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(recovered, how='left', on=['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

#preprocessing
covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['recovered'] = covid_data['recovered'].fillna(0)
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']
covid_data1 = covid_data.groupby(['date'])[['confirmed', 'death', 'recovered', 'active']].sum().reset_index()

app = dash.Dash(__name__, )
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('ethanlee.png'),
                     id='corona-image')
        ], className='one-third column'),
        
        html.Div([
            html.Div([
                html.H3('Covid-19'),
                html.H5('Track Covid-19 Cases')
            ])
        ], className='one-half column', id='title'),
        
        html.Div([
            html.H6('Last Updated: ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y') + ' 00:01 (UTC)'))
        ], className='one-third column', id='title1')
    ], id='header', className='row flex-display'),
    
    html.Div([
        html.Div([
            html.H6(children='Global cases'),
            html.P(f"{covid_data1['confirmed'].iloc[-1]:,.0f}"),
            html.P(f"New : {round(covid_data1['confirmed'].iloc[-1] - covid_data1['confirmed'].iloc[-2], 3):,.0f} 🔺")
        ], className='card-container three columns'),
        
        html.Div([
            html.H6(children='Global deths'),
            html.P(f"{covid_data1['death'].iloc[-1]:,.0f}"),
            html.P(f"New : {round(covid_data1['death'].iloc[-1] - covid_data1['death'].iloc[-2], 3):,.0f} 🔺")
        ], className='card-container three columns'),
        
        html.Div([
            html.H6(children='Global recovered'),
            html.P(f"{covid_data1['recovered'].iloc[-1]:,.0f}"),
            html.P(f"New : {round(covid_data1['recovered'].iloc[-1] - covid_data1['recovered'].iloc[-2], 3):,.0f} 🔺")
        ], className='card-container three columns'),
        
        html.Div([
            html.H6(children='Global active'),
            html.P(f"{covid_data1['active'].iloc[-1]:,.0f}"),
            html.P(f"New : {round(covid_data1['active'].iloc[-1] - covid_data1['active'].iloc[-2], 3):,.0f} 🔺")
        ], className='card-container three columns'),
    ], className='row flex display')
    
    
], id='main-container')

if __name__ == '__main__' :
    app.run_server(debug=True)