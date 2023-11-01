from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar, dash_rb, dash_cpu,dash_interfaces,infrastructure

#from globals import *


# =========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
    #dcc.Store(id='store-receitas', data=df_receitas.to_dict()),
    #dcc.Store(id='store-despesas', data=df_despesas.to_dict()),

    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        dbc.Col([
            content
        ], md=10)
    ])

], fluid=True,)

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/dash_rb':
        return dash_rb.layout
    elif pathname == '/rb_cpu':
        return dash_cpu.layout
    elif pathname == '/rb_interfaces':
        return dash_interfaces.layout
    elif pathname == '/infrastructure':
        return infrastructure.layout
    else:
        return '404'






if __name__ == '__main__':
    app.run_server(port=65100, debug=True)