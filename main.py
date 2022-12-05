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
    html.P("Select the data according to users: ",style={'margin':'40px'}),
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

#Component 2 Pie Chart

pie_component = html.Div([
    html.P("Select the time for which you want to see personal records values:",style={'margin':'40px'}),
    dcc.Dropdown(id='values',
        options=df['Time'].unique().tolist(),
        value=df['Time'].unique().tolist()[0], clearable=False,
        style={"text-align":"center",'width':'200px'}
    ),
    dcc.Graph(id="graph_p")

])


@app.callback(
    Output("graph_p", "figure"), 
    # Input("names", "value"), 
    Input("values", "value"))
def generate_chart(values):
    labels = ['CC','EA','TCA','TQA']
    n=f'Time=="{values}"'
    nf = df.query(n)

    values = [nf.personalRecords_CC.tolist()[0],nf.personalRecords_EA.tolist()[0],nf.personalRecords_TCA.tolist()[0],
          nf.personalRecords_TQA.tolist()[0]]

    fig = px.pie(nf, values=values, names=labels, hole=.3,labels=labels)
    # fig = px.pie(df, values=values, names=names, hole=.3)
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
            [html.P('Pie Chart for Values of personal records in a particular moment of time',style={'text-align':'center','padding':'4px','margin-top':'40px','font-size':'25px','color':'darkcyan'}),
        pie_component        ]
        ),
        dbc.Row(
            [html.P('Total time spent according to the respective users with respect to date and time',style={'text-align':'center','padding':'4px','margin-top':'40px','font-size':'25px','color':'darkcyan'}),
            barchart_component],style={'background-color':'floralwhite'}
        ),
    ],style={'background-color':'floralwhite'},
    
)
#Run the App
app.run_server(debug=True)