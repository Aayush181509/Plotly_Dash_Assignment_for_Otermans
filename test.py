from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
app = Dash(__name__)

df=pd.read_csv("data/IDC_new_Data.csv")


app.layout = html.Div([
    html.H4('Analysis of the restaurant sales'),
    dcc.Graph(id="graph_p"),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=df['Time'].unique().tolist(),
        value=df['Time'].unique().tolist()[0], clearable=False
    ),
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


app.run_server(debug=True)