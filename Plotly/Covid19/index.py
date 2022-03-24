import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

def data_unpivot(url, value_name) :
    df = pd.read_csv(url)
    date = df.columns[4:]
    total = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date, var_name = 'date', value_name = value_name)
    return total

confirmed = data_unpivot(url_confirmed, 'confirmed')
deaths = data_unpivot(url_deaths, 'deaths')
recovered = data_unpivot(url_recovered, 'recovered')

print(confirmed.tail())