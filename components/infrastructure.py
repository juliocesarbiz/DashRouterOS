# Import packages
import pandas as pd
import dash
from dash import Dash, html,  dcc
import dash_daq as daq
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.express as px

from pymongo import MongoClient

from app import app

# Conectar ao banco de dados MongoDB
uri = "mongodb+srv://martins:LlmN6xS3wBMHTMch@cluster0.he6wly3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database = client['ufsc']

Atualizacao_grafico = 0
uso_cpu = 0


def verifica_lista_portas(data):
    collection = database['rb_interface']

    # Passo 1: Executar a primeira consulta para obter os valores distintos
    distinct_values = collection.distinct("name")
    print(distinct_values)

    # Passo 2: Usar o resultado da primeira consulta na segunda consulta
    subquery_result = collection.find({'name': {'$in': distinct_values}})
    df = pd.DataFrame(subquery_result)
    lista_interfaces = pd.unique(df[data])

    # Fechar conexão com o MongoDB
    #client.close()

    return lista_interfaces


# Inicializando o aplicativo Dash
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
layout = dbc.Container([
    dcc.Store(id='store-nome-interface', data=verifica_lista_portas('name')),

    html.Div(id='output-provider'),

    dbc.Col([
        dbc.Row([
             dbc.Col([
                 dbc.Label('Descrição: '),
             ], width=1),
            dbc.Col([
                 dbc.Input(placeholder="Ex.:Descrição dispositivo", id="txt-device-description"),
             ], width=4),     
        ]),
        html.Br(),
        dbc.Row([
             dbc.Col([
                 dbc.Label('IP: '),
             ], width=1),
            dbc.Col([
                 dbc.Input(placeholder="Ex.:192.168.1.88", id="txt-ip-address"),
             ], width=4),     
        ]),
        html.Br(),
        dbc.Row([
             dbc.Col([
                 dbc.Label('Senha: '),
             ], width=1),
            dbc.Col([
                 dbc.Input(id="txt-pw-device", type='password'),
             ], width=4),     
        ]),
        dbc.Button(
            "Salvar", id="bt-save", className="d-grid gap-2 col-2 mx-auto", n_clicks=0
        ),
    ],style={'padding': '30px'}),

])

# =========  Callbacks  =========== #
