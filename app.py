import pandas as pd
import datetime
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

# data source
data_raw_url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
data_raw = pd.read_csv(data_raw_url)



data_count = pd.crosstab(data_raw['Accurate_Episode_Date'], data_raw['Reporting_PHU'])
data_count.index = pd.DatetimeIndex(data_count.index)
date_new = pd.date_range(start=data_count.index.min(), end=data_count.index.max())
date_count = data_count.reindex(date_new, fill_value=0)
data_cumul = data_count


options = [
    {'label': 'York Region Public Health Services', 'value': 'York Region Public Health Services'},
    {'label': 'Region of Waterloo, Public Health', 'value': 'Region of Waterloo, Public Health'},
    {'label': 'Simcoe Muskoka District Health Unit', 'value': 'Simcoe Muskoka District Health Unit'},
    {'label': 'Peel Public Health', 'value': 'Peel Public Health'},
    {'label': 'Windsor-Essex County Health Unit', 'value': 'Windsor-Essex County Health Unit'},
    {'label': 'Chatham-Kent Health Unit', 'value': 'Chatham-Kent Health Unit'},
    {'label': 'Halton Region Health Department', 'value': 'Halton Region Health Department'},
    {'label': 'Durham Region Health Department', 'value': 'Durham Region Health Department'},
    {'label': 'Toronto Public Health', 'value': 'Toronto Public Health'},
    {'label': 'Ottawa Public Health', 'value': 'Ottawa Public Health'},
    {'label': 'Brant County Health Unit', 'value': 'Brant County Health Unit'},
    {'label': 'Wellington-Dufferin-Guelph Public Health', 'value': 'Wellington-Dufferin-Guelph Public Health'},
    {'label': 'Middlesex-London Health Unit', 'value': 'Middlesex-London Health Unit'},
    {'label': 'Southwestern Public Health', 'value': 'Southwestern Public Health'},
    {'label': 'Niagara Region Public Health Department', 'value': 'Niagara Region Public Health Department'},
    {'label': 'Hamilton Public Health Services', 'value': 'Hamilton Public Health Services'},
    {'label': 'Kingston, Frontenac and Lennox & Addington Public Health',
     'value': 'Kingston, Frontenac and Lennox & Addington Public Health'},
    {'label': 'Lambton Public Health', 'value': 'Lambton Public Health'},
    {'label': 'Leeds, Grenville and Lanark District Health Unit',
     'value': 'Leeds, Grenville and Lanark District Health Unit'},
    {'label': 'Hastings and Prince Edward Counties Health Unit',
     'value': 'Hastings and Prince Edward Counties Health Unit'},
    {'label': 'Huron Perth District Health Unit', 'value': 'Huron Perth District Health Unit'},
    {'label': 'Eastern Ontario Health Unit', 'value': 'Eastern Ontario Health Unit'},
    {'label': 'Peterborough Public Health', 'value': 'Peterborough Public Health'},
    {'label': 'Northwestern Health Unit', 'value': 'Northwestern Health Unit'},
    {'label': 'Algoma Public Health Unit', 'value': 'Algoma Public Health Unit'},
    {'label': 'Haldimand-Norfolk Health Unit', 'value': 'Haldimand-Norfolk Health Unit'},
    {'label': 'Haliburton, Kawartha, Pine Ridge District Health Unit',
     'value': 'Haliburton, Kawartha, Pine Ridge District Health Unit'},
    {'label': 'Grey Bruce Health Unit', 'value': 'Grey Bruce Health Unit'},
    {'label': 'North Bay Parry Sound District Health Unit', 'value': 'North Bay Parry Sound District Health Unit'},
    {'label': 'Sudbury & District Health Unit', 'value': 'Sudbury & District Health Unit'},
    {'label': 'Renfrew County and District Health Unit', 'value': 'Renfrew County and District Health Unit'},
    {'label': 'Thunder Bay District Health Unit', 'value': 'Thunder Bay District Health Unit'},
    {'label': 'Porcupine Health Unit', 'value': 'Porcupine Health Unit'},
    {'label': 'Timiskaming Health Unit', 'value': 'Timiskaming Health Unit'},
]

# In[8]:


app = dash.Dash()
server = app.server
app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=options,
        value='Haldimand-Norfolk Health Unit'
    ),
    html.Div([dcc.Graph(id='graph1')]), html.Div([dcc.Graph(id='graph2')]),

])


@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_figure(phu):
    y_count = data_count[phu]
    y_cumul = data_count[phu].cumsum()
    data_bar = go.Bar(x=data_count.index, y=y_count, name='Daily count of COVID-19 cases')
    data_scatter = go.Scatter(x=data_count.index, y=y_cumul, yaxis="y2", name='Cumulative count of COVID-19 cases')
    layout = go.Layout(title='Covid-19 disease trend for ' + str(phu),
                       yaxis2=dict(title='Cumulative frequency', side='right', overlaying='y', color='red',
                                   rangemode='nonnegative', showgrid=False)
                       , yaxis=dict(title='Daily count', color='blue', showgrid=True),
                       legend=dict(orientation='h')
                       )

    fig = go.Figure(data=[data_bar, data_scatter],
                    layout=layout)

    return fig


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def rolling(phu):
    y_rolling_avg_14 = data_count[phu].rolling(14).mean()
    y_cumul = data_count[phu].cumsum()
    data_scatter2 = go.Scatter(x=data_count.index, y=y_rolling_avg_14,
                               name='14-day rolling average of COVID-19 cases related to ' + phu )
    layout2 = go.Layout(title='14-day rolling average for ' + phu,
                        yaxis=dict(title='14-day rolling average', color='blue', showgrid=True,
                                   rangemode='nonnegative'),
                        legend=dict(orientation='h')
                        )

    fig2 = go.Figure(data=data_scatter2,
                     layout=layout2)

    return fig2


if __name__ == '__main__':
    app.run_server()







