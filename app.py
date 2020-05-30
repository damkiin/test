#awon modulu ti mo ma lo
import pandas as pd
import datetime
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

# data source ni website ijoba ontario
data_raw_url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
data_raw = pd.read_csv(data_raw_url)

#Grouping the data bi mo shey fe
data_count = pd.crosstab(data_raw['Accurate_Episode_Date'], data_raw['Reporting_PHU'])
data_count.index = pd.DatetimeIndex(data_count.index)
date_new = pd.date_range(start=data_count.index.min(), end=data_count.index.max())
date_count = data_count.reindex(date_new, fill_value=0)
data_cumul = data_count

option = [{'label': phus, 'value': phus} for phus in data_raw['Reporting_PHU'].unique()]

#The dash app gaangaan
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Div(html.H1('COVID-19 TREND (ONTARIO HEALTH UNITS)', style=dict(textAlign='center')), className="row"),
    html.Div(['Text box'], className="row"),
    html.Div(html.Label('Select health unit'), style=dict(color='blue', textAlign='center')),
    html.Div([dcc.Dropdown(
        id='demo-dropdown',
        options=option,
        value='',
        style=dict(width='50%', fontweight='bold', margin='auto', textAlign='center')
    )], className="row"),
    html.Div([
        html.Div([dcc.Graph(id='graph1')], className="eight columns"),
        html.Div([dcc.Graph(id='graph2')], className="four columns"),
    ], className="row"),
    html.Div([
        html.Div([dcc.Graph(id='graph6')], className="four columns"),
        html.Div([dcc.Graph(id='graph7')], className="eight columns"),
    ], className="row"),
    html.Div([
        html.Div([dcc.Graph(id='graph3')], className="four columns"),
        html.Div([dcc.Graph(id='graph4')], className="four columns"),
        html.Div([dcc.Graph(id='graph5')], className="four columns"),
    ], className="row"),

    html.Div(['row5'], className="row"),
    html.Div(['row6'], className="row"),
    html.Div(['row7'], className="row"),
    html.Div(['row8'], className="row"),
])


@app.callback(dash.dependencies.Output('graph1', 'figure'),
              [dash.dependencies.Input('demo-dropdown', 'value')])
def graph1(phu):
    y_count = data_count[phu]
    y_cumul = data_count[phu].cumsum()
    data_bar = go.Bar(x=data_count.index, y=y_count, name='Daily count of COVID-19 cases')
    data_scatter = go.Scatter(x=data_count.index, y=y_cumul, yaxis="y2", name='Cumulative count of COVID-19 cases')
    layout = go.Layout(title='Covid-19 disease trend for ' + str(phu),
                       yaxis2=dict(title='Cumulative frequency', side='right', overlaying='y', color='red',
                                   rangemode='nonnegative', showgrid=False, fixedrange=True),
                       yaxis=dict(title='Daily count', color='blue', showgrid=True, fixedrange=True),
                       xaxis=dict(fixedrange=True),
                       legend=dict(orientation='h')
                       )

    fig = go.Figure(data=[data_bar, data_scatter],
                    layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph2(phu):
    x = data_raw.groupby(by='Reporting_PHU').get_group(phu)
    y = 'Outcome1'
    data1 = go.Pie(labels=pd.value_counts(x[y]).index, values=pd.value_counts(x[y]), hole=.5, textinfo='label+percent')
    layout1 = go.Layout(title=y, showlegend=False)
    fig2 = go.Figure(data=data1, layout=layout1)
    return fig2


@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph3(phu):
    x = data_raw.groupby(by='Reporting_PHU').get_group(phu)
    y = 'Client_Gender'
    data1 = go.Pie(labels=pd.value_counts(x[y]).index, values=pd.value_counts(x[y]), hole=.5, textinfo='label+percent')
    layout1 = go.Layout(title=y, showlegend=False)
    fig3 = go.Figure(data=data1, layout=layout1)
    return fig3


@app.callback(
    dash.dependencies.Output('graph4', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph4(phu):
    x = data_raw.groupby(by='Reporting_PHU').get_group(phu)
    y = 'Age_Group'
    data1 = go.Pie(labels=pd.value_counts(x[y]).index, values=pd.value_counts(x[y]), hole=.5, textinfo='label+percent')
    layout1 = go.Layout(title=y, showlegend=False)
    fig4 = go.Figure(data=data1, layout=layout1)
    return fig4


@app.callback(
    dash.dependencies.Output('graph5', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph5(phu):
    x = data_raw.groupby(by='Reporting_PHU').get_group(phu)
    y = 'Case_AcquisitionInfo'
    data1 = go.Pie(labels=pd.value_counts(x[y]).index, values=pd.value_counts(x[y]), hole=.5, textinfo='label+percent')
    layout1 = go.Layout(title=y, showlegend=False)
    fig5 = go.Figure(data=data1, layout=layout1)
    return fig5


@app.callback(
    dash.dependencies.Output('graph6', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph6(phu):
    x = data_raw.groupby(by='Reporting_PHU').get_group(phu)
    y = 'Outbreak_Related'
    data1 = go.Pie(labels=pd.value_counts(x[y]).index, values=pd.value_counts(x[y]), hole=.5, textinfo='label+percent')
    layout1 = go.Layout(title=y, showlegend=False)
    fig6 = go.Figure(data=data1, layout=layout1)
    return fig6


@app.callback(
    dash.dependencies.Output('graph7', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def graph8(phu):
    y_rolling_avg_14 = data_count[phu].rolling(14).mean()
    y_cumul = data_count[phu].cumsum()
    data_scatter2 = go.Scatter(x=data_count.index, y=y_rolling_avg_14,
                               name='14-day rolling average of COVID-19 cases related to ' + phu)
    layout2 = go.Layout(title='14-day rolling average for ' + phu,
                        yaxis=dict(title='14-day rolling average', color='blue', showgrid=True,
                                   rangemode='nonnegative', fixedrange=True),
                        legend=dict(orientation='h'),
                        xaxis=dict(fixedrange=True)
                        )
    fig7 = go.Figure(data=data_scatter2,
                     layout=layout2)
    return fig7


if __name__ == '__main__':
    app.run_server()






