# Import packages
import os
import pandas as pd
import dash
from dash import Dash, html,  dcc, dash_table
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



    dbc.Row([
        html.Legend('DataRouter', style={"text-align": "center"}),
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Status das Interfaces'),
                html.Div(id='tabela-interface', className='dbc'),                
            ], style={'height': '100%', 'padding':'10px' })
        ],  width=12),  
    ]),
    dbc.Row([
        dcc.Interval(
            id='interval-component3',
            interval=60000,  # Atualiza o gráfico a cada 2 segundos
            n_intervals=0
        )
    ])

])

# =========  Callbacks  =========== #




# Atualiza o gráfico de linhas com os dados do banco de dados
@app.callback(
    Output('tabela-interface', 'children'),
    [
    Input('interval-component3', 'n_intervals')
    ]
)

def imprimir_tabela(n):

    collection = database['rb_interface'].find().sort('data-hora',-1).limit(14)  # Limitando a 10 registros
    df_original = pd.DataFrame(collection).sort_values('default-name')

    colunas_selecionadas = ['.id','default-name','type', 'link-downs', 'last-link-down-time','data-hora','disabled','running']
    df = df_original[colunas_selecionadas].copy()
    #
    df = df.rename(columns={'.id': 'id'})
    df = df.rename(columns={'default-name': 'Nome'})
    df = df.rename(columns={'type': 'Tipo'})
    df = df.rename(columns={'link-downs': 'Quedas de Link'})
    df = df.rename(columns={'last-link-down-time': 'Última queda'})
    df = df.rename(columns={'disabled': 'Desabilitada'})
    df = df.rename(columns={'running': 'Status'})

    df['Status'] = df['Status'].apply(lambda x: "OK" if x == "true" else "Sem Conexão" if x == "false" else x)
    df['Desabilitada'] = df['Desabilitada'].apply(lambda x: 'sim' if x == "true" else "não" if x == "false" else x)
    df = df.set_index('id')

    print ("data frame")
    print(df)

    df = df.fillna('-')

    #df.sort_values(by='data', ascending=False)

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
                'column_id': 'Status',
            },
            'backgroundColor': 'dodgerblue',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Status} != OK && {Desabilitada} = não',
                'column_id': 'Status'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Quedas de Link} <= 2',
                'column_id': 'Quedas de Link'
            },
            'backgroundColor': 'dodgerblue',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Quedas de Link} > 2  && {Quedas de Link}  <=5',
                'column_id': 'Quedas de Link'
            },
            'backgroundColor': 'orange',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Quedas de Link} > 5',
                'column_id': 'Quedas de Link'
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        }
    ])

    return tabela

