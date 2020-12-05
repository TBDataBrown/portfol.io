import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px 
import pandas as pd  

from database import fetch_all_bpa_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions


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
        # Executive Summary
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

        Kevin Le


        Xiongfeng (Alex) Wang


        Shuya Zhang


        Adrian Lam
        
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")



def nextsteps():
    """
    Next steps
    """
    return html.Div(children=[dcc.Markdown('''
        # Our Next Steps
        
        
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
        nextsteps(),
        refs(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components below



if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
