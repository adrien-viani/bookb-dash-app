import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


df = pd.read_csv('https://gist.githubusercontent.com/'
                 'adrien-viani/a05fc36e640f9ec1881f4a434e620014/'
                 'raw/fac8a41dddfeca88bf23525dde9ad431b306edbb/bookb_data.csv')
df['fee_per_avg_dwn'] = df['Free']/df['Avg Dwnlds']

available_region = df['Region'].unique()
spec_col = list(df.columns)[2:7]


bookb_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = bookb_app.server

bookb_app.layout = html.Div([
    html.H1(children = 'Bookbub Featured Deal Pricing', style = {'background-color': '#E31E27', 
                                              'color': '#FFFFFF', 'font-family': 'Arial',
                                              'font-weight': 'bold','width':'52%' }),
    html.Div(children='''
        Dashboard for top 10 subscriber genres, by region. Select a Region.
    '''),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': i, 'value': i} for i in available_region],
                value='All'
                        )
                ], style={'width': '49%'}),
        html.Div([
        dcc.Graph(
            id='subscriber-bar'
        )
        ], style={'display': 'inline-block', 'width': '49%'}),
        html.Div([
        dcc.Graph(
            id='fee-grouped-bar'
        )
        ], style={'display': 'inline-block', 'width': '49%'}),
        html.Div([
        dcc.Graph(
            id='fee-per-avg-down'
        )
        ], style={'display': 'inline-block', 'width': '98%'}),
        ])
])
       
@bookb_app.callback(
    dash.dependencies.Output('subscriber-bar', 'figure'),
    [dash.dependencies.Input('region-filter', 'value')])
def update_bar(selected_region):
    filtered_df = df[df['Region']==selected_region]
    categ_list = list(filtered_df['Category'])
    trace0 = go.Bar(
    x = categ_list,
    y = list(filtered_df['Subscribers']),
    text = ['&#43;']*10,
    hoverinfo ='y+text',
    hoverlabel= {'bordercolor' : 'rgb(0,0,0)'},
    marker = {'color':'rgb(227, 30, 39)'}
    
    )
    return {
    'data' : [trace0],
    'layout': go.Layout(
    margin={'b': 90,'r': 110},
    title = 'Subscriber Count by Genre, Top 10 Subscribed Genres',
    yaxis = {'title' : '# of Subscribers+'}
    )
    }
    
@bookb_app.callback(
    dash.dependencies.Output('fee-per-avg-down', 'figure'),
    [dash.dependencies.Input('region-filter', 'value')])
def update_fee_dwn_bar(selected_region):
    filtered_df = df[df['Region']==selected_region]
    categ_list = list(filtered_df['Category'])
    trace0 = go.Bar(
    x = categ_list,
    y = list(filtered_df['fee_per_avg_dwn']),
    hoverinfo ='y',
    hoverlabel= {'bordercolor' : 'rgb(0,0,0)'},
    marker = {'color':'rgb(227, 30, 39)'}
    )
    return {
    'data' : [trace0],
    'layout': go.Layout(
    margin={'b': 90,'r': 110},
    title = '&#36; Cost Per Download, Top 10 Subscribed Genres<br>(Using Avg Campaign Download)',
    yaxis = {'title' : 'Cost Per Download','hoverformat' : '$,.4f'}
    )
    }
 
@bookb_app.callback(
    dash.dependencies.Output('fee-grouped-bar', 'figure'),
    [dash.dependencies.Input('region-filter', 'value')])
def update_grouped_bar(selected_region):
    filtered_df = df[df['Region']==selected_region]
    categ_list = list(filtered_df['Category'])
    traces = []
    for col in spec_col:
        traces.append(go.Bar(
        x=categ_list,
        y=filtered_df[col],
        name = col,
        hoverinfo = 'y'
        ))
    return {
    'data' : traces,
    'layout': go.Layout(
    barmode = 'group',
    margin={'b': 90,'r': 110},
    title = 'Bookbub Fee by Promotional Price, Top 10 Subscribed Genres',
    yaxis = {'title' : 'Fee by Promo Price', 'hoverformat' : '$,.4f'}
    )
    }           
            
if __name__ == '__main__':
    bookb_app.run_server()