# Import packages
import os
import pandas as pd
import dash
from dash import Dash, html,  dcc
import dash_daq as daq
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.express as px

from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

from app import app

# Conectar ao banco de dados MongoDB
client = MongoClient(os.environ["uri_banco"])
database = client[os.environ["Database_Name"]]

Atualizacao_grafico = 0
uso_cpu = 0


def verifica_lista_portas(data):

    collection = database['rb_interface']
    distinct_values = collection.distinct("name")
    print('lista portas distintas')
    print(distinct_values)

    return distinct_values


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
