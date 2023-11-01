# Import packages
import os
import pandas as pd
import dash
from dash import Dash, html,  dcc
import dash_daq as daq
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px

from pymongo import MongoClient

from app import app

# Conectar ao banco de dados MongoDB
uri = "mongodb+srv://martins:LlmN6xS3wBMHTMch@cluster0.he6wly3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database = client['ufsc']

Atualizacao_grafico = 0

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
    dbc.Row([
        html.Legend('DataRouter',
                        style={"text-align": "center"}),
        html.Div(id='dash-monitoramento-cpu', className='dbc'),
        html.Br()

    ]),
    dbc.Row([
        dcc.Graph(id='graph-cpu')
    ]),
    dbc.Row([
        dcc.Interval(
            id='interval-component2',
            interval=4000,  # Atualiza o gráfico a cada 2 segundos
            n_intervals=0
        )
    ])
])

# =========  Callbacks  =========== #


# Atualiza o gráfico de linhas com os dados do banco de dados
@app.callback(
    Output('graph-cpu', 'figure'),
    [
    Input('interval-component2', 'n_intervals')
    ]
)

def update_line_chart2(n):

    #filtro = {'name':{'$in':data_nome_interface}}
    #print("filtro")
    #print (filtro)
    data = database['rb_sytem'].find().sort('data-hora').limit(2000)  # Limitando a 10 registros

    df = pd.DataFrame(data)
    print ("data frame")
    print(df)

    # Armazenar o tipo de dados original da coluna
    dtype_original = df['free-hdd-space'].dtype
    df['free-hdd-space'] = df['free-hdd-space'].astype(float).apply(lambda x: 100 - (x * 100 / 1074790400))
    df['free-hdd-space'] = df['free-hdd-space'].astype(dtype_original)

    # Armazenar o tipo de dados original da coluna
    dtype_original = df['free-memory'].dtype
    df['free-memory'] = df['free-memory'].astype(float).apply(lambda x: 100 - (x * 100 / 1073741824))
    df['free-memory'] = df['free-memory'].astype(dtype_original)

    # Armazenar o tipo de dados original da coluna
    dtype_original = df['cpu-frequency'].dtype
    df['cpu-frequency'] = df['cpu-frequency'].astype(float).apply(lambda x: x / 14)
    df['cpu-frequency'] = df['cpu-frequency'].astype(dtype_original)



    global Atualizacao_grafico
    Atualizacao_grafico += 1
    print ("atualização numero")
    print (Atualizacao_grafico)

    # Verificar o tipo de dados da coluna1
    print(df['cpu-frequency'].dtype)

    # Gerando o gráfico de linhas duplas
    fig = px.line(df, x='data-hora', y=['cpu-load', 'cpu-frequency', 'cpu-temperature','free-memory','free-hdd-space'], title='Uso de CPU')
    fig.update_layout(autotypenumbers='convert types')

    return fig

