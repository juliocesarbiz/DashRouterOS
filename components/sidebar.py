import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd


#from globals import *

import pdb

# ========= Layout ========= #
layout = dbc.Col([
        html.H1("MIkrotik", className="text-primary"),
        html.P("By TI", className="text-info"),
        html.Hr(),

         #seção Perfil
    dbc.Button(id='botao_avatar',
        children=[html.Img(src='/assets/img_home.png', id='avatar_charge', alt='Avatar', className='perfil_avatar', width="100", height="100",)
    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),

  
    html.Hr(),
    dbc.Row([
    
    #Seção NAV
   
    #html.Legend('DataRouter', style={"text-align": "center"}),
    dbc.Nav([
        dbc.NavLink("Geral", href="/", active="exact"),
        dbc.NavLink("Sistema", href="/rb_cpu", active="exact"),
        dbc.NavLink("Interfaces", href="/rb_interfaces", active="exact"),
        dbc.NavLink("Dispositivos", href="/infrastructure", active="exact"),
    ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom":"50px"}),
    ], id='sidebar_completa'),

    #tml.I(class="fa-solid fa-cube")
 
])

        





# =========  Callbacks  =========== #
# Pop-up receita
