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

option = [{'label': phus, 'value': phus} for phus in data_raw['Reporting_PHU'].unique()]

# In[8]:


app = dash.Dash()
server = app.server
app.layout = html.Div(children = [
    html.Div(html.H1('COVID-19 TRENDS (ONTARIO HEALTH UNITS)', style= dict(textAlign= 'center'))),
    html.Div(html.Label('Select health unit'), style= dict(color = 'blue', textAlign= 'center')),
    html.Div([dcc.Dropdown(
        id='demo-dropdown',
        options=option,
        value='',
        style= dict(width = '50%', fontweight = 'bold', margin = 'auto', textAlign= 'center')
    ),
    html.Div([
        html.Div([dcc.Graph(id='graph1', style=dict())]),
        html.Div([dcc.Graph(id='graph2', style=dict())]),
    ])

])])


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
                                   rangemode='nonnegative', showgrid=False,fixedrange = True),
                       yaxis=dict(title='Daily count', color='blue', showgrid=True, fixedrange = True),
                       xaxis = dict(fixedrange = True),
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
                               name='14-day rolling average of COVID-19 cases related to ' + phu)
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







