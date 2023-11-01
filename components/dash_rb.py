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

    dbc.Row([
        dbc.Row([
            html.Legend('DataRouter',
                        style={"text-align": "center"}),
            html.Div(id='dash-monitoramento', className='dbc'),
            html.Br()
        ]),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Uso de CPU'),
                       daq.GraduatedBar(
                        id='graduated-bar-cpu',
                        showCurrentValue=True,
                        max=100,
                    ),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    id='card_uso_cpu',
                    color='LightSkyBlue',
                    style={'maxWidth': 75, "height": 120, 'margin-left': '-10px'}
                )
            ],style={'height':120})
        ], width=4),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Frequência CPU'),
                    daq.GraduatedBar(
                        id='graduated-bar-cpu-frequency',
                        showCurrentValue=True,
                        max=100,
                    ),
                    html.H5("100 Mhz", id='p-cpu-frequency-dashboard', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(

                    id='card_frequencia_cpu',
                    color='LightSkyBlue',
                    style={'maxWidth': 75, "height": 120, 'margin-left': '-10px'}
                )
            ],style={'height':120})
        ], width=4,),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Temperatura CPU'),
                    daq.GraduatedBar(
                        id='graduated-bar-cpu-temperature',
                        showCurrentValue=False,
                        max=100,
                    ),
                    html.H5("20 ºC", id='p-cpu-temperature-dashboard', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                dbc.Card(
                    html.Div(className='fa fa-university' """style=card_icon"""),
                    id='card_temp_cpu',
                    color='LightSkyBlue',
                    style={'maxWidth': 75, "height": 120, 'margin-left': '-10px'}
                )
            ], style={'height': 120})
        ], width=4),

    ]),
    dbc.Row([
        dcc.Graph(id='graph1')
    ]),
    dbc.Row([
        html.Label("Interfaces"),
        html.Div(
            dcc.Dropdown(
                id="dropdown-nome-interfaces",
                clearable=False,
                style={"width": "100%"},
                persistence=True,
                persistence_type="session",
                multi=True)
        ),
    ]),
    dbc.Row([
        dcc.Interval(
            id='interval-component',
            interval=4000,  # Atualiza o gráfico a cada 2 segundos
            n_intervals=0
        )
    ])
])

# =========  Callbacks  =========== #

# Atualiza o gráfico de linhas com os dados do banco de dados
@app.callback(
    Output('graph1', 'figure'),
    [
    Input('interval-component', 'n_intervals'),
    Input("dropdown-nome-interfaces", "value")
    ]
)

def update_line_chart(n, data_nome_interface):

    filtro = {'name':{'$in':data_nome_interface}}
    print("filtro")
    print (filtro)
    data = database['rb_monitor_traffic'].find(filtro).sort('data-hora',-1).limit(1500)  # Limitando a 10 registros

    df = pd.DataFrame(data)
    print ("data frame")
    print(df)

    global Atualizacao_grafico
    Atualizacao_grafico += 1
    print ("atualização numero")
    print (Atualizacao_grafico)

    # Gerando o gráfico de linhas duplas
    fig = px.line(df, x='data-hora', y=['rx-bits-per-second', 'tx-bits-per-second'], title='Grafico 1')
    fig.update_layout(autotypenumbers='convert types')

    return fig


#Lista interfaces
@app.callback(
    [
        Output("dropdown-nome-interfaces", "options"),
        Output("dropdown-nome-interfaces", "value")
    ],
    Input("store-nome-interface", "data")
)

def populate_dropdown_values(data):
    df=pd.DataFrame(data)
    val = df[0]

    return ([{"label":x, "value": x} for x in val], val)



#graduated_bar_cpu
@app.callback(
    [
        Output("graduated-bar-cpu","value"),
        Output("graduated-bar-cpu-frequency","value"),
        Output("p-cpu-frequency-dashboard","children"),
        Output("graduated-bar-cpu-temperature","value"),
        Output("p-cpu-temperature-dashboard","children"),
    ],
    Input('interval-component', 'n_intervals'),
)

def cb_graduated_bar(n):
    global uso_cpu
    data_sys = database['rb_sytem'].find().sort('data-hora',-1).limit(1)  # Limitando a 10 registros

    df_sys = pd.DataFrame(data_sys)

    cpu_l  = [df_sys.iloc[0]['cpu-load']]
    cpu_f = df_sys.iloc[0]['cpu-frequency']
    cpu_f2 = [int(df_sys.iloc[0]['cpu-frequency'])/14]  # converte para escalar 0..100 grafico barras
    cpu_t  = [df_sys.iloc[0]['cpu-temperature']]
    cpu_t2 = df_sys.iloc[0]['cpu-temperature']

    uso_cpu = cpu_t2

    return (cpu_l, cpu_f2,f"{cpu_f} Mhz", cpu_t, f"{cpu_t2} ºC")
