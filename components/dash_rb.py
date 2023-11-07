# Import packages
import os
import pandas as pd
import re
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

    dcc.ConfirmDialog(
        id='confirm-danger',
        message='Alerta: ',
    ),


    dbc.Row([
        dbc.Row([
            html.Legend('DataRouter',
                        style={"text-align": "center"}),
            html.Div(id='dash-monitoramento', className='dbc'),
            html.Br()
        ]),
        html.Br(),
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
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Uptime'),
                    html.H5("10 Dias", id='p-uptime-rb', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Modelo'),
                    html.H5("txt", id='p-board-name', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([           
                    html.Legend('Arquitetura'),
                    html.H5("txt", id='p-architecture-name', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Atualização'),
                    html.H5("01/01/2023", id='p-build-time', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
       dbc.Col([
            dbc.CardGroup([   
                dbc.Card([
                    html.Legend('Firmware'),
                    html.H5("01/01/2023", id='p-firmware-version', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
        dbc.Col([
            dbc.CardGroup([   
                dbc.Card([
                    html.Legend('Bad Blocks'),
                    html.H5("0", id='p-bad-blocks', style={}),
                ], style={'padding-left': '20px', 'padding-top': '10px'}),
            ],style={'height':120})
        ], width=2,),
    ]),
    
    html.Br(),
    dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph-ping'),
                    html.Div([
                dbc.Button(
                    "Sobre Estatísticas de Servidor DNS",
                    id="collapse-button-dns",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody("É utilizado para monitorar a qualidade da rede e a latência, além disso detectar quedas de conexão com o provedor de internet.")),
                    id="collapse-dns",
                    is_open=False,
                ),
            ])
        ],style={'height': '100%', 'padding':'10px' } )
    ],  width=12),
    html.Br(),
    
    dbc.Col([
       
        dbc.Card([
            html.Label("Neighbour Discovery"),
            html.Br(),
            html.Div(id='tabela-neighbors', className='dbc'),
            html.Br(),
            html.Div([
                dbc.Button(
                    "Sobre Neighbour Discovery",
                    id="collapse-button",
                    className="mb-3",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody("Os protocolos Neighbour Discovery nos permitem encontrar dispositivos compatíveis com MNDP (MikroTik Neighbor Discovery Protocol), CDP (Cisco Discovery Protocol) ou LLDP (Link Layer Discovery Protocol) no transmissão da Camada2. Ele pode ser usado para mapear sua rede.")),
                    id="collapse",
                    is_open=False,
                ),
            ])
        ],style={'height': '100%', 'padding':'10px' } )
    ],  width=12),
    html.Br(),
    
    dbc.Col([
        dbc.Card([
            dcc.Graph(id='graph1'),
            html.Label("Interfaces"),
            html.Div(
                dcc.Dropdown(
                    id="dropdown-nome-interfaces",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True)),
        ],style={'height': '100%', 'padding':'10px' } )
    ],width=12),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dcc.Interval(
            id='interval-component',
            interval=4000,  # Atualiza o gráfico a cada 2 segundos
            n_intervals=0
        )
    ])
])

# =========  Callbacks  =========== #


##----------------------------------------------------------------
## Atualiza o gráfico de tráfego 
##----------------------------------------------------------------

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


    # Gerando o gráfico de linhas duplas
    fig = px.line(df, x='data-hora', y=['rx-bits-per-second', 'tx-bits-per-second'], title='Estatísticas de tráfego por interface')
    fig.update_layout(yaxis_title="Mbps")

    fig.update_layout(autotypenumbers='convert types')

    return fig

##----------------------------------------------------------------
## Atualiza o tabela neighbors
##----------------------------------------------------------------
@app.callback(
    Output('tabela-neighbors', 'children'),
    [
    Input('interval-component', 'n_intervals')
    ]
)

def tabela_neighbors(n):

    collection = database['rb_neighbors'].find().sort('data-hora',-1).limit(3)  # Limitando a 10 registros
    df_original = pd.DataFrame(collection).sort_values('mac-address')

    colunas_selecionadas = ['.id','interface','mac-address', 'identity','platform','version','address','uptime', 'board']
    df = df_original[colunas_selecionadas].copy()
    #
    df = df.rename(columns={'.id': 'id'})
    df = df.rename(columns={'identity': 'Nome'})
    df = df.rename(columns={'platform': 'platforma'})
    df = df.rename(columns={'version': 'versão'})
    df = df.rename(columns={'address': 'Endereço'})

    df = df.set_index('id')
    df = df.fillna('-')

    tabela = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    return tabela

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-dns", "is_open"),
    [Input("collapse-button-dns", "n_clicks")],
    [State("collapse-dns", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
##----------------------------------------------------------------
## Atualiza o gráfico de latencia de ping
##----------------------------------------------------------------

@app.callback(
    Output('graph-ping', 'figure'),
    Input('interval-component', 'n_intervals')
)

def update_graph_ping(n):

    data = database['rb_ping'].find().sort('data-hora',-1).limit(300)  # Limitando a 10 registros
    #data = database['rb_monitor_traffic'].find(filtro).sort('data-hora',-1).limit(1500) 
    df = pd.DataFrame(data)
    print ("data frame")
    print(df)
    df['avg-rtt_ms'] = df['avg-rtt'].apply(lambda x: int(re.search(r'(\d+)ms(\d+)us', x).group(1)) + int(re.search(r'(\d+)ms(\d+)us', x).group(2)) / 1000 if re.search(r'(\d+)ms(\d+)us', x) else 0)
    df['time_ms'] = df['time'].apply(lambda x: int(re.search(r'(\d+)ms(\d+)us', x).group(1)) + int(re.search(r'(\d+)ms(\d+)us', x).group(2)) / 1000 if re.search(r'(\d+)ms(\d+)us', x) else 0)

    # Gerando o gráfico de linhas duplas
    fig = px.line(df, x='data-hora', y=['avg-rtt_ms','time_ms'], title='Ping Servidores DNS')
    fig.update_layout(yaxis_title="Milissegundo (ms)")
    fig.update_layout(autotypenumbers='convert types')

    return fig


##----------------------------------------------------------------
## Lista interfaces
##----------------------------------------------------------------

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


##----------------------------------------------------------------
## Graduated_bar_cpu
##----------------------------------------------------------------

@app.callback(
    [
        Output("graduated-bar-cpu","value"),
        Output("graduated-bar-cpu-frequency","value"),
        Output("p-cpu-frequency-dashboard","children"),
        Output("graduated-bar-cpu-temperature","value"),
        Output("p-cpu-temperature-dashboard","children"),

        Output("p-uptime-rb","children"),
        Output("p-board-name","children"),
        Output("p-architecture-name","children"),
        Output("p-build-time","children"),
        Output("p-firmware-version","children"),
        Output("p-bad-blocks","children"),
        
    ],
    Input('interval-component', 'n_intervals'),
)

def cb_graduated_bar(n):
    global uso_cpu
    data_sys = database['rb_sytem'].find().sort('data-hora',-1).limit(1)  

    df_sys = pd.DataFrame(data_sys)

    cpu_l  = [df_sys.iloc[0]['cpu-load']]
    cpu_f = df_sys.iloc[0]['cpu-frequency']
    cpu_f2 = [int(df_sys.iloc[0]['cpu-frequency'])/14]  # converte para escalar 0..100 grafico barras
    cpu_t  = [df_sys.iloc[0]['cpu-temperature']]
    cpu_t2 = df_sys.iloc[0]['cpu-temperature']

    uptime = df_sys.iloc[0]['uptime']
    board_name = df_sys.iloc[0]['board-name']
    architecture = df_sys.iloc[0]['architecture-name']
    build_time = df_sys.iloc[0]['build-time']
    version = df_sys.iloc[0]['version']
    bad_blocks = df_sys.iloc[0]['bad-blocks']

    uso_cpu = cpu_l

    return (cpu_l, cpu_f2,f"{cpu_f} Mhz", cpu_t, f"{cpu_t2} ºC",uptime,board_name,architecture,build_time,version,bad_blocks)



##----------------------------------------------------------------
## Alertas
##----------------------------------------------------------------

@app.callback(
    Output('confirm-danger', 'displayed'),
    Input('interval-component', 'n_intervals')
)
def display_confirm(value):
    data_sys = database['rb_sytem'].find().sort('data-hora',-1).limit(1)  
    df_sys = pd.DataFrame(data_sys)
    cpu_l  = [df_sys.iloc[0]['cpu-load']]


    if (int(cpu_l[0]) > 1):
        return True
    return False