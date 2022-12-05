#importing modules 
import dash
from dash import dcc,html,dcc,html,Input,Output,Dash
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from dash import Dash, dcc, html, Input, Output
#initiating the app
server=Flask(__name__)
app=dash.Dash(__name__,server =server,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])


# Reading the files which we created in csv format
df1=pd.read_csv("data/Users_Data.csv")
df=pd.read_csv("data/IDC_new_Data.csv")
