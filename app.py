import dash   
import dash_core_components as dcc   
import dash_html_components as html  
import plotly.express as px 
import pandas as pd  

external_stylesheets = []
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)