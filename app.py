import dash   
import dash_core_components as dcc   
import dash_html_components as html  
import plotly.express as px 
import pandas as pd  
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go 
import chart_studio.plotly as py
import plotly.figure_factory as ff

# borrowing function from database
from database import fetch_all_stock_as_df

# Definition of constants. This project uses extra CSS stylesheet at `./assets/style.css.html`
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,title='Portfol.io')

### Define component functions

def random_color():
    color = tuple(np.random.choice(range(256), size=3))
    color = 'rgb'+str(color)
    return color


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Portfol.io')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('TBData', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a0d4b6',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/TBDataBrown'),
    ], className="row")

def summary():
    """
    Returns executive summary in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # About Portfol.io
        Portfol.io is an interactive portfolio manager that aims to simplify and streamline
        the way individual investors calculate and visualize their returns.
        Numerous financial websites and APIs out there track stock prices and indices, but they are often 
        clunky and tedious to use, and any analysis of the data requires substantial technical know-how.
        With Portfol.io, the TBData team wanted to create a one-stop shop for savvy
        investors to curate, visualize, and analyze their investments in an intuitive manner.
        Functionalities include:
        - Automatically updated real-time visualizations of stock prices and related data
        - Forecasting of stock prices with an LSTM model
        - Retrieve and visualize historical market data, up to 1 minute in granularity
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

def team():
    """
    Team members
    """
    return html.Div(children=[dcc.Markdown('''
        # The TBData Team
        - Kevin Le
        - Xiongfeng (Alex) Wang
        - Shuya Zhang
        - Adrian Lam
        
        ''', className='eleven columns', style={'paddingLeft': '5%', 'marginTop':'1.5rem'})], className="row")


def static_stacked_trend_graph(stack=False):
    """Returns static visualization of stock prices over last 7 days"""
    df = fetch_all_stock_as_df()
    if df is None: 
        return go.Figure()
    tickers = ['TSLA', 'ENPH', 'ZM', 'MRNA', 'PTON', 'BTBT', 'TGT', 'WMT', 'SBUX', 'ABBV']
    x = df['Datetime']

    fig = go.Figure()
    for i,s in enumerate(tickers):
        fig.add_trace(go.Scatter(x=x, y=df[s],mode='lines', name=s, 
        line={'width':2, 'color': random_color()}, 
        stackgroup='stack' if stack else None))
    title = 'Selected Stock Prices over 7 Days'
    if stack:
        title += ' [Stacked]'

    fig.update_xaxes(
    rangebreaks=[
        dict(bounds=[21, 14.5], pattern="hour"),
    ])

    fig.update_layout(template='ggplot2',
                    title=title,
                    yaxis_title='Stock Price per Share',
                    xaxis_title='Date/Time for Trading Hours'
    )

    return fig


def interactive_portfolio_description():
    """
    Returns description of interactive porfolio component.
    """
    return html.Div(children=[
        dcc.Markdown('''
        # Interactive Portfolio
        We curated a list of 10 top stocks from Investopedia advisors, considering factors including
        value, growth, and dividends in the month of December 2020. These stocks come from technology,
        energy, consumer products, and healthcare sectors. With Portfol.io, you can choose from the 10 stocks
        and specify the number of shares of each stock. Our visualizer will show your portfolio's performance over the 
        last 7 days and compare it with the performance of major indexes, including the Dow Jones Industrial, Nasdaq Composite,
        and S&P 500.
        ''', className='eleven columns', style={'paddingLeft':'5%', 'marginTop':'1.5rem'})
    ], className='row')

def nextsteps():
    """
    Next steps
    """
    return html.Div(children=[dcc.Markdown('''
        # Next Steps
        In future iterations of Portfol.io, we plan on releasing new features that allow users to 
        add their stocks of choice to their portfolio, rather than be limited to a fixed set of stocks. 
        Additionally, users will be able to visualize their porfolio's short-term and long-term performance trends
        by allowing users to change the interval of their portfolio. These new features would allow individual investors to make more informed investment
        decisions. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

def refs():
    """
    References of related work
    """
    return html.Div(children=[dcc.Markdown('''
        # Related Work
        [Prabhakaran, S. (2020, September 17). ARIMA Model - Complete Guide to Time Series Forecasting in Python.]
        (https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/)

        [Loukas, S. (2020, July 31). LSTM Time-Series Forecasting: Predicting Stock Prices Using An LSTM Model.] 
        (https://towardsdatascience.com/lstm-time-series-forecasting-predicting-stock-prices-using-an-lstm-model-6223e9644a2f)

        [Nayak, A. (2020, June 10). Predicting Stock Price with LSTM.]
        (https://towardsdatascience.com/predicting-stock-price-with-lstm-13af86a74944)
    
        ''', className='eleven columns', style={'paddingLeft': '5%', 'marginTop':'1.5rem'})], className="row")

# Interactive portfolio tool 
def interactive_portfolio_tool():
    """
    Returns the interactive portfolio manager as a dash `html.Div`. The view
    is a 8:3 division between a graph showing portfolio performance and input boxes 
    to allocate shares to stocks. 
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='interactive-portfolio')], className='nine columns'),
        html.Div(children=[
            html.H5("Stocks & Number of Shares", style={'marginTop':'0.5rem', 'fontSize':18}), 
            # big div containing 10 subdivs which provide 
            # stock name (ticker) + input box for shares
            html.Div(children=[
                # subdiv 1: Tesla + input box
                html.Div(children=[
                    html.H6("Tesla (TSLA)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}), 
                    dcc.Input(
                        id='tsla',
                        type='number',
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%', 'marginTop':'1rem', 'display':'inline-table', 'verticalAlign':'middle'}),
                # subdiv 2: Enphase Energy + input box
                html.Div(children=[
                    html.H6("Enphase (ENPH)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='enph',
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 3: Zoom + input box
                html.Div(children=[
                    html.H6("Zoom (ZM)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='zm',
                        type='number',
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 4: Moderna + input box
                html.Div(children=[
                    html.H6("Moderna (MRNA)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='mrna',
                        type='number',
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 5: Peloton + input box
                html.Div(children=[
                    html.H6("Peloton (PTON)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='pton', 
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 6: Bit Digital + input box
                html.Div(children=[
                    html.H6("Bit Digital (BTBT)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='btbt',
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 7: Target + input box
                html.Div(children=[
                    html.H6("Target (TGT)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='tgt', 
                        type='number',
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 8: Walmart + input box
                html.Div(children=[
                    html.H6("Walmart (WMT)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id ='wmt', 
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 9: Starbucks + input box
                html.Div(children=[
                    html.H6("Starbucks (SBUX)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='sbux',
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 10: Abbvie + input box
                html.Div(children=[
                    html.H6("Abbvie (ABBV)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='abbv',
                        type='number', 
                        min=1, max=1000, step=1,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'})
            ])
        ], className='three columns', style={'marginLeft': 5, 'marginTop':'2.5%'})
    ], className='row twelve columns', style={'marginBottom':'10%'})

# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        summary(),
        team(),
        dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        interactive_portfolio_description(),
        interactive_portfolio_tool(),
        nextsteps(),
        refs(),
    ], className='row', id='content')

# Set layout to a function which updates upon reloading 
app.layout = dynamic_layout()

# Defines dependencies of interactive components

@app.callback(
    Output(component_id='interactive-portfolio', component_property='figure'),
    [Input('tsla', 'value'),
    Input('enph', 'value'),
    Input('zm', 'value'), 
    Input('mrna', 'value'), 
    Input('pton', 'value'),
    Input('btbt', 'value'), 
    Input('tgt', 'value'), 
    Input('wmt', 'value'), 
    Input('sbux', 'value'),
    Input('abbv', 'value')]
)
def interactive_portfolio_handler(tsla, enph, zm, mrna, pton, btbt, tgt, wmt, sbux, abbv):
    """Changes the display graph of our interactive portfolio"""
    
    fig = go.Figure()
    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)



