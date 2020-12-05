import dash   
import dash_core_components as dcc   
import dash_html_components as html  
import plotly.express as px 
import pandas as pd  
from dash.dependencies import Input, Output
import plotly.graph_objects as go 

# borrowing function from database
from database import fetch_all_stock_as_df

# Definition of constants. This project uses extra CSS stylesheet at `./assets/style.css.html`
COLORS = ['rgb(51,153,102)', 'rgb(0,102,204)', 'rgb(255,0,0)', 'rgb(255,102,0)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,title='Portfol.io')

### Define component functions

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
                                                'paddingLeft': '4px', 'color': '#f6c154',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/TBDataBrown'),
    ], className="row")

def summary():
    """
    Returns executive summary in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Overview
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
        
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

# Visualization 
# Kevin: we want to extract just the close price for each day
# our short interval is producing the noisy look of our graphs
def static_stacked_trend_graph(stack=False):
    df = fetch_all_stock_as_df()
    if df is None: 
        return go.Figure()
    tickers = ['SBUX', 'AAPL']
    x = df['Datetime']
    fig = go.Figure()
    for i,s in enumerate(tickers):
        fig.add_trace(go.Scatter(x=x, y=(df[s].pct_change()+1).cumprod(),mode='lines', name=s, 
        line={'width':2, 'color': COLORS[i]}, 
        stackgroup='stack' if stack else None))
    title = 'Selected Stock Prices over 7 Days'
    if stack:
        title += ' [Stacked]'
    
    fig.update_layout(template='ggplot2',
                    title=title,
                    yaxis_title='Stock Price per Share',
                    xaxis_title='Date/Time')
    return fig

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
    Adrian: We should probably make the reference name a hyperlink instead of listing the url; I will do this tomorrow
    """
    return html.Div(children=[dcc.Markdown('''
        # Related Work
        Prabhakaran, S. (2020, September 17). ARIMA Model - Complete Guide to Time Series Forecasting in Python. 
        Retrieved November 15, 2020, from https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/
        Loukas, S. (2020, July 31). LSTM Time-Series Forecasting: Predicting Stock Prices Using An LSTM Model. 
        Retrieved November 15, 2020, from https://towardsdatascience.com/lstm-time-series-forecasting-predicting-stock-prices-using-an-lstm-model-6223e9644a2f
        Nayak, A. (2020, June 10). Predicting Stock Price with LSTM. Retrieved November 15, 2020, 
        from https://towardsdatascience.com/predicting-stock-price-with-lstm-13af86a74944
        
        
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        summary(),
        team(),
        dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        nextsteps(),
        refs(),
    ], className='row', id='content')

# Set layout to a function which updates upon reloading 
app.layout = dynamic_layout()

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)



