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
server = app.server

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
        - Retrieve and visualize historical market data, up to 1 minute in granularity
        - Devise a personalized portfolio and compare performance to market indices
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

def static_graph_description():
    """Description for static visualization"""
    return html.Div(children=[
        dcc.Markdown('''
        # Real Time Stock Prices
        Interactive stock chart displaying real-time stock prices for ten high-performing stocks. 
        Hover over a particular line to track that stock’s price at any instant of time! 
        Chart is continuously updated on trading days as data comes in.
        ''', className='eleven columns', style={'paddingLeft': '5%', 'marginTop':'1.5rem'})], className='row')


def static_stacked_trend_graph(stack=False):
    """Returns static visualization of stock prices over last 7 days"""
    df = fetch_all_stock_as_df()
    if df is None: 
        return go.Figure()
    tickers = ['TSLA', 'AMD', 'ZM', 'MRNA', 'PTON', 'AAPL', 'TGT', 'WMT', 
    'SBUX', 'ABBV', 'NIO', 'SPY']
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
        dict(bounds=["sat", "mon"]) # hide weekends
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
        value, growth, and dividends in the month of December 2020. These stocks come from a variety of industries, 
        including the technology, energy, consumer products, and healthcare sectors. With Portfol.io, you can choose from the 10 stocks
        and specify the number of shares of each stock. Our visualizer will show your portfolio's performance over the 
        last 7 days and compare it with the performance of major indices, including the Dow Jones Industrial
        and S&P 500.
        ''', className='eleven columns', style={'paddingLeft':'5%', 'marginTop':'1.5rem'})
    ], className='row')

def project_details():
    """
    Returns descriptions about details of the project
    """
    return html.Div(children=[
        dcc.Markdown('''
        # Project Details
        The final product drew from various resources and made use of a wide range of available technology, 
        ranging from yfinance and MongoDB to plotly and Dash. First off, our data is accessed through the **yfinance API**, 
        which allows for mass access to real-time stock market data from Yahoo! finance. Upon extraction, our data is stored in a **MongoDB** database in raw form.
        A built-in function ensures updates are pulled through as new data comes in throughout the trading day. The dashboard itself is a **Dash app**, and the interactive visualizations were created in conjunction with *plotly*. 
        Finally, our Dash app is hosted on **Heroku**.

        You can view our ETL procedure and prototypes for our visualizations below:

        [ETL_EDA]
        (https://github.com/TBDataBrown/portfol.io/blob/main/EDA_ETL.ipynb)

        [Visualization prototype]
        (https://github.com/TBDataBrown/portfol.io/blob/main/Enhancement.ipynb)

        ''', className='eleven columns', style={'paddingLeft':'5%', 'marginTop':'1.5rem'})
    ], className='row')

def nextsteps():
    """
    Next steps
    """
    return html.Div(children=[dcc.Markdown('''
        # Next Steps
        In future iterations of Portfol.io, we plan on releasing new features that allow users to 
        add their stocks of choice to their portfolio, rather than a fixed list of stocks. 
        Additionally, users will be able to visualize their porfolio's short-term and long-term performance trends
        by allowing users to change the interval of their portfolio.
        ''', className='eleven columns', style={'paddingLeft': '5%', 'marginTop':'1.5rem'})], className="row")

def refs():
    """
    References of related work
    """
    return html.Div(children=[dcc.Markdown('''
        # Related Work
        [yfinance API by Ran Aroussi]
        (https://github.com/ranaroussi/yfinance)

        [Aroussi, R. (2019, April 17). Guide to yfinance API by its creator]
        (https://aroussi.com/post/python-yahoo-finance)

        [Bland, G. (2020, November 03). Yahoo Finance API - A Complete Guide]
        (https://algotrading101.com/learn/yahoo-finance-api-guide/)

        [Boller, K. (2018, April 16). Python for Finance: Stock Portfolio Analyses]
        (https://towardsdatascience.com/python-for-finance-stock-portfolio-analyses-6da4c3e61054)

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
                        min=0, max=9999999, step=1,
                        value=0,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%', 'marginTop':'1rem', 'display':'inline-table', 'verticalAlign':'middle'}),
                # subdiv 2: AMD + input box
                html.Div(children=[
                    html.H6("AMD (AMD)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='amd',
                        type='number', 
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 6: Apple + input box
                html.Div(children=[
                    html.H6("Apple (AAPL)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='aapl',
                        type='number', 
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
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
                        min=0, max=9999999, step=1,
                        value=0,
                        placeholder='Shares',
                        style={'display':'table-cell'}
                    )
                ], style={'width':'100%','display':'inline-table', 'verticalAlign':'middle', 'marginTop':'0.5rem'}),
                # subdiv 11: Nio + input box
                html.Div(children=[
                    html.H6("Nio (NIO)", style={'fontSize':14, 'marginTop':'0.5rem', 'display':'table-cell'}),
                    dcc.Input(
                        id='nio', 
                        type='number', 
                        min=0, max=9999999, step=1,
                        value=0, 
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
        static_graph_description(),
        dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        interactive_portfolio_description(),
        interactive_portfolio_tool(),
        project_details(),
        nextsteps(),
        refs(),
    ], className='row', id='content')

# Set layout to a function which updates upon reloading 
app.layout = dynamic_layout()

# Defines dependencies of interactive components

@app.callback(
    dash.dependencies.Output('interactive-portfolio', 'figure'),
    [dash.dependencies.Input('tsla', 'value'),
    dash.dependencies.Input('amd', 'value'),
    dash.dependencies.Input('zm', 'value'), 
    dash.dependencies.Input('mrna', 'value'), 
    dash.dependencies.Input('pton', 'value'),
    dash.dependencies.Input('aapl', 'value'), 
    dash.dependencies.Input('tgt', 'value'), 
    dash.dependencies.Input('wmt', 'value'), 
    dash.dependencies.Input('sbux', 'value'),
    dash.dependencies.Input('abbv', 'value'),
    dash.dependencies.Input('nio', 'value')]
)
def interactive_portfolio_handler(tsla, amd, zm, mrna, pton, aapl, tgt, wmt, sbux, abbv, nio):
    """Changes the display graph of our interactive portfolio"""
    df = fetch_all_stock_as_df()
    x = df['Datetime']

    SPY = df['SPY']
    base_spy = df['SPY'][0]
    SPY = (SPY/base_spy-1)*100

    DJI = df['^DJI']
    base_dji = df['^DJI'][0]
    DJI = (DJI/base_dji-1)*100

    fig = go.Figure()
    title = "Portfolio Performance vs. S&P500 & Dow Jones Industrial"
    # SPY line
    fig.add_trace(go.Scatter(x=x, y=SPY, mode='lines', name='S&P 500', 
    line=dict(color='red', width=2)))
    # DJI line
    fig.add_trace(go.Scatter(x=x, y=DJI, mode='lines', name='Dow Jones Industrial',
    line=dict(color='blue', width=2)))

    ptf = df['TSLA']*tsla + df['AMD']*amd + df['ZM']*zm + df['MRNA']*mrna + df['PTON']*pton + \
        df['AAPL']*aapl + df['TGT']*tgt + df['WMT']*wmt + df['SBUX']*sbux + df['ABBV']*abbv + \
        df['NIO']*nio
    base_ptf = df['TSLA'][0]*tsla + df['AMD'][0]*amd + df['ZM'][0]*zm + df['MRNA'][0]*mrna + df['PTON'][0]*pton + \
        df['AAPL'][0]*aapl + df['TGT'][0]*tgt + df['WMT'][0]*wmt + df['SBUX'][0]*sbux + df['ABBV'][0]*abbv + \
        df['NIO'][0]*nio
    ptf = (ptf/base_ptf-1)*100

    # Portfolio line
    fig.add_trace(go.Scatter(x=x, y=ptf, mode='lines', name='Portfolio',
    line=dict(color='green', width=2)))

    fig.update_layout(template='ggplot2', title=title, yaxis_title='Net Gain (USD)',
    xaxis_title='Date/Time for Trading Hours')

    fig.update_xaxes(
    rangebreaks=[
        dict(bounds=[21, 14.5], pattern="hour"),
        dict(bounds=["sat", "mon"])
    ])

    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)



