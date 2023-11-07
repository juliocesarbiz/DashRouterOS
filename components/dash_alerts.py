# Import packages
import os
import pandas as pd
import dash
from dash import Dash, html,  dcc,dash_table
import dash_daq as daq
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px

from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

from app import app

# Conectar ao banco de dados MongoDB
client = MongoClient(os.environ["uri_banco"])
database = client[os.environ["Database_Name"]]

Atualizacao_grafico = 0



# Inicializando o aplicativo Dash
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
layout = dbc.Container([
  
    dbc.Row([
        html.Legend('DataRouter',
                        style={"text-align": "center"}),
        html.Div(id='dash-monitoramento-cpus', className='dbc'),
        html.Br()

    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                html.Legend('Últimos alertas'),
                html.Div(id='tabela-alerts', className='dbc'),
            ], style={'height': '100%', 'padding':'10px' }),  width=12
        ),  
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
    Output('tabela-alerts', 'children'),
    [
    Input('interval-component2', 'n_intervals')
    ]
)

def update_linse_chart2(n):

    #filtro = {'name':{'$in':data_nome_interface}}
    #print("filtro")
    #print (filtro)
    dados = {
    'Alertas': ['USO CPU 100%', 'USO CPU 75%', 'Atualização Disponível', 'Temperatura CPU elevada', 'Teste de ping (50 % pacotes perdidos)', 'Teste de ping (50 % pacotes perdidos)'],
    'Criticidade': ['Alta', 'Média', 'Baixa', 'Alta', 'Média', 'Média'],
    'Data': ['20/11/2023','21/11/2023','23/11/2023','01/12/2023','01/12/2023','01/12/2023'],
    'Hora': ['02:35:10','10:09:59','14:20:34','01:41:10','12:20:33','12:22:41']
}


   
    df = pd.DataFrame(dados)
 

    global Atualizacao_grafico
    Atualizacao_grafico += 1


    # Gerando o gráfico de linhas duplas
    tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                      style_header={
            'backgroundColor': 'SteelBlue',
            'color': 'Azure'
        },
        style_data={
            'backgroundColor': 'Azure',
            'color': 'black'
        },
         style_data_conditional =[


        {
            'if': {
                'filter_query': '{Criticidade} = Alta',
                'column_id': 'Criticidade'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        }
        ])
    

    return tabela

