#importing modules 
import dash
from dash import dcc,html,dcc,html,Input,Output,Dash
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


#initiating the app
server=Flask(__name__)
app=dash.Dash(__name__,server =server,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])


# Reading the files which we created in csv format
df1=pd.read_csv("data/Users_Data.csv")
df=pd.read_csv("data/IDC_new_Data.csv")



#Build The Components
# Component 1 Barchart
barchart_component=html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=["krizia", "peri peri", "pradip", "sirupate","yash"],
        value="krizia",
        clearable=False,
        style={"text-align":"center",'width':'200px'}
    ),
    dcc.Graph(id="graph_bar"),
])

@app.callback(
    Output("graph_bar", "figure"), 
    Input("dropdown", "value"))

def update_bar_chart(name):
    mask=df['name']==name
    fig = px.bar(df[mask], x="Time", y="timeSpent_total", 
                 color="Date")
    return fig



# Designing the app layout

app.layout=html.Div(
    [   html.H1('Dashboard',style={'text-align':'center','padding':'4px','margin':'4px','color':'darkcyan'}),
        dbc.Row(
            [html.P('Total Time Spent By Users according to days',style={'padding':'4px','margin':'40px','font-size':'25px','color':'darkcyan'}),
            dcc.Graph(figure=go.Figure(px.bar(df,x='Date',y='timeSpent_total',color='Time',facet_col='name')))]
        ),
        dbc.Row(
            [dbc.Col(
               [html.P('Pie Chart for time spent by users at different sections',style={'text-align':'center','padding':'4px','margin-top':'40px','font-size':'25px','color':'darkcyan'}),
                dcc.Graph(figure=go.Figure(data=[go.Pie(labels=['AI','HomeScreen','Lesson',
                                  'Maps','Quiz','RewardPage','Store'],
                          values=[df['timeSpent_timeAI'].sum(),df['timeSpent_timeHomeScreen'].sum(),df['timeSpent_timeLesson'].sum(),
                                 df['timeSpent_timeMaps'].sum(),df['timeSpent_timeQuiz'].sum(),df['timeSpent_timeRewardPage'].sum(),
                                 df['timeSpent_timeStore'].sum()])]))],style={'background-color':'floralwhite'}
                
            ),dbc.Col(
                [html.P('Pie Chart for time spent by users at different sections',style={'text-align':'center','padding':'4px','margin-top':'40px','font-size':'25px','color':'darkcyan'}),
                dcc.Graph(figure=go.Figure(px.pie(df,values='timeSpent_total',names='name',hole=.2)))],style={'background-color':'floralwhite'}
            )]
        ),
        dbc.Row(
            [html.P('Pie Chart for time spent by users at different sections',style={'text-align':'center','padding':'4px','margin-top':'40px','font-size':'25px','color':'darkcyan'}),
            barchart_component],style={'background-color':'floralwhite'}
        )
    ],style={'background-color':'floralwhite'}
)
#Run the App
app.run_server(debug=True)