import pandas as pd
import plotly
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output

ecss=[{
    "href":"https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
    "rel":"stylesheet",
    "integrity":"sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC",
    "crossorigin":"anonymous"}]
options=[
    {"label":"All","value":"All"},
    {"label":"Hospitalised","value":"Hospitalized"},
    {"label":"Recovered","value":"Recovered"},
    {"label":"Deaths","value":"Deceased"}


]
patient=pd.read_csv("IndividualDetails.csv")

app = dash.Dash(__name__,external_stylesheets=ecss)
app.layout = html.Div([
    html.H1("Corona Virus DashBoard",className=" text-center mt-5",style={'backgroundColor':'white'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases"),
                    html.H4(patient.shape[0])
                ],className="card-body")
            ],className="card bg-danger text-light")
        ],className="col-md-3"),
        html.Div([ html.Div([
                html.Div([
                    html.H3("Hospitalised"),
                    html.H4(patient["current_status"].value_counts()[0])
                ],className="card-body")
            ],className="card bg-warning text-light")],className="col-md-3"),
        html.Div([ html.Div([
                html.Div([
                    html.H3("Recovered"),
                    html.H4(patient["current_status"].value_counts()[1])
                ],className="card-body")
            ],className="card bg-success text-light")],className="col-md-3"),
        html.Div([ html.Div([
                html.Div([
                    html.H3("Death"),
                    html.H4(patient["current_status"].value_counts()[2])
                ],className="card-body")
            ],className="card bg-danger text-light")],className="col-md-3")
    ],className="row mt-5"),
    html.Div([
        html.Div([
            dcc.Graph(id="line",figure={"data":[go.Scatter(x=patient[
                "diagnosed_date"].value_counts().sort_values(ascending=True).reset_index()[
                "diagnosed_date"],y=patient["diagnosed_date"].value_counts().sort_values(ascending=
                True).reset_index()["count"])],"layout":go.Layout(title="Date wise Analysis")})
        ],className="col-md-6 mt-5"),
        html.Div([
            dcc.Graph(id="pie",figure={"data":[go.Pie(values=patient["gender"].value_counts().values,labels=
            patient["gender"].value_counts().index)],"layout":go.Layout(title="Gender wise Analysis")})
        ],className="col-md-6 mt-5")
    ],className="row"),
    html.Div([
        html.Div([
            dcc.Dropdown(id="dropdown",options=options,value="All"),
            dcc.Graph(id="bar")
        ],className="col-md-12")
    ],className="row mt-5")
],className="container")

@app.callback(Output("bar","figure"),
              [Input("dropdown","value")])
def update(choice):
    if choice == "All":
        return{"data":[go.Bar (x= patient["detected_state"].value_counts().index,
                               y=patient["detected_state"].value_counts().values)]}
    else:
        return {"data":[go.Bar(x = patient["detected_state"][patient["current_status"]==choice].value_counts().index,
                               y=patient["detected_state"][patient["current_status"]==choice].value_counts().values)]}
app.run_server(debug =True)