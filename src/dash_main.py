# Este es la aplicacion final con el dash

# Se puede ejecutar con este comando en la consola de Python desde el root del proyecto
# exec(open('src/dash_main.py').read())

# Tambien se puede ejecutar desde una terminal, tambien desde la raiz del proyecto
# python src/dash_main.py

import sys
sys.path.append('src/')
import dictionaries
import mapa
import mapaDensidad
import mapaPrecio
import pie
import pieClusters
import violin
import lineas
import viz_forecast


import time, datetime
import pickle
import dash, logging
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from PIL import Image

# Read geojsons
exec(open('src/dash_declarations.py').read())

with open("data/output/df_parsed", 'rb') as f:
    df_parsed_1 = pickle.load(f)

product="gasoline_95E5"

def getDropdownDistritos():
    """
    Output:
    distritos: lista de str. Lista con los distritos de madrid
    """
    distritos = dictionaries.list_distritos
    distritos.insert(0, "Todos")
    return distritos



def filtrarDF(producto, distrito, start_date, end_date, barrio, cluster):
    """
    Parameters:
    producto: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    return_df: df. dataframe con los datos filtrados en funcion de los filtros
    """
    with open("data/output/dict_df_products_clustering_2", 'rb') as f:
        dict_df_products = pickle.load(f)
    return_df = dict_df_products[producto]

    if len(return_df):
        if cluster != 'Todos':
            return_df = return_df[return_df['Cluster']==cluster]

    if len(return_df):
        if distrito != 'Todos':
            return_df = return_df[return_df['district']==distrito]

    if len(return_df):
        if barrio != 'Todos':
            return_df = return_df[return_df['neighbourhood']==barrio]

    if len(return_df):
        return_df = return_df[(return_df['date']>= start_date) & (return_df['date']<= end_date)]

    return return_df


def getMapa(id, prod, distrito, start_date, end_date, barrio, cluster):
    """
    Devuelve un mapa que puede ver:
     La densidad de gasolineras por barrio
     El precio medio del combustible por barrio
     La localizacion exacta de las gasolineras, junto a su tama??o (numero de productos ofrecidos) y su empresa

    Parameters:
    id: str. Tipo de mapa a representar
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Mapa a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date, barrio, cluster)
    if id == 'id_Localizacion':
        fig = mapa.crearMapaScatter(df)
    elif id == 'id_Densidad':
        fig = mapaDensidad.crearMapaDensidad(df)
    else:
        fig = mapaPrecio.crearMapaPrecio(df, prod)

    return fig



def getPie(prod, distrito, start_date, end_date, barrio, cluster):
    """
    Pie chart que representa la cuota del total de gasolineras seleccionadas que posee cada compa??ia

    Parameters:
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Piechart a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date, barrio, cluster)
    fig=pie.crearPie(df)

    return fig

def getPieCluster(prod, distrito, start_date, end_date, barrio, cluster):
    """
    Pie chart que representa, del total de gasolineras seleccionadas, cuantas pertenecen a cada cluster

    Parameters:
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Piechart a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date, barrio, cluster)
    fig = pieClusters.crearPieCluster(df)

    return fig

def getViolinEmpresas(prod, distrito, start_date, end_date, barrio, cluster):
    """
    Grafica de violin que representa la distribucion del precio del combustible seleccionado

    Parameters:
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Grafica de violin a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date , barrio, cluster)
    fig = violin.crearViolinEmpresas(df, prod)

    return fig

def getLineas(prod, distrito, start_date, end_date, barrio, cluster):
    """
    Grafica de lineas que representa la evolucion temporal del precio del combustible seleccionado

    Parameters:
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Grafica de lineas a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date, barrio, cluster)
    fig=lineas.crearLineas(df, prod)

    return fig

def getForecast(prod, distrito, start_date, end_date, barrio, cluster):
    """
    Grafica de lineas que representa la evolucion temporal del precio AJUSTADO del combustible seleccionado y su forecast

    Parameters:
    prod: str. nombre del combustible
    distrito: str. nombre del distrito
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Grafica de lineas a representar
    """

    df = filtrarDF(prod, distrito, start_date, end_date, barrio, cluster)
    fig=viz_forecast.crearForecast(df, prod, cluster)

    return fig


app = dash.Dash(suppress_callback_exceptions=False,
                external_stylesheets=[dbc.themes.LUX])
app.title = "GeoPortal"

#logging.getLogger('werkzeug').setLevel(logging.INFO)
dash.register_page(__name__, path='/')


app.layout = dbc.Container(
    [
        dbc.Row([ # Primera fila
            dbc.Col([ # Primera fila/primer bloque
                html.Img(src=Image.open('resources/gas-station-icon.png'),
                         style={
                             "width": "35%"
                         },
                         className="rounded mx-auto d-block"
                )
                ],
                width={"size": 2}
            ),
            dbc.Col([ # Primera fila/segundo bloque
                html.H1("Estudio de las gasolineras en la ciudad de Madrid",
                        style={
                            "fontSize": "50",
                            "horizontal-align": "center",
                            "textAlign": "center",
                            "color": "black",
                        }
                ),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=min(df_parsed_1['date']),
                    max_date_allowed=max(df_parsed_1['date']),
                    start_date=min(df_parsed_1['date']),
                    end_date=max(df_parsed_1['date']),
                    style=
                        {
                            "text-align":"center",
                            "width": "100%",
                            "margin-top": "1%",
                        }
                )

            ]#,
                #width={"size": 8},
            ),
            dbc.Col([ # Primera fila/tercer bloque
                html.Img(src=Image.open('resources/madrid-logo.png'),
                         style={
                             "width": "35%",
                             "vertical-align": "center",
                             "textAlign": "center",
                            "horizontal-align": "right"
                         },
                        className="rounded mx-auto d-block"
                )
                ],
                width={"size": 2}
            )
        ],
            id="cabecera-general",
            style={
                "padding-top": "1%",
            },
            justify="evenly"
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="district-dd",
                        options= getDropdownDistritos(),
                        value='Todos',
                        placeholder="Distrito",
                        clearable=False,
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="barrio-dd",
                        options=["Todos"],
                        value='Todos',
                        clearable=False,
                    )
                )
            ],
            id="row-dropdown-distritos",

        ),
        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="95E5",             style={'padding': '0'},     tab_id="gasoline_95E5"),
                                    dbc.Tab(label="95E5 Premium",     style={'padding': '0'},     tab_id="gasoline_95E5_premium"),
                                    dbc.Tab(label="98E5",             style={'padding': '0'},     tab_id="gasoline_98E5"),
                                    #dbc.Tab(label="98E10",            style={'padding': '0'},     tab_id="gasoline_98E10"),
                                    dbc.Tab(label="Diesel A",         style={'padding': '0'},     tab_id="diesel_A"),
                                    dbc.Tab(label="Diesel B",         style={'padding': '0'},     tab_id="diesel_B"),
                                    dbc.Tab(label="Diesel Premium",   style={'padding': '0'},     tab_id="diesel_premium"),
                                    #dbc.Tab(label="Bioetanol",        style={'padding': '0'},     tab_id="bioetanol"),
                                    dbc.Tab(label="Biodiesel",        style={'padding': '0'},     tab_id="biodiesel"),
                                    dbc.Tab(label="LPG",              style={'padding': '0'},     tab_id="lpg"),
                                    dbc.Tab(label="CNG",              style={'padding': '0'},     tab_id="cng"),
                                    dbc.Tab(label="LNG",              style={'padding': '0'},     tab_id="lng"),
                                    #dbc.Tab(label="Hidr??geno",        style={'padding': '0'},     tab_id="hydrogen"),
                                    #dbc.Tab(label="Comparativa",      style={'padding': '0'},     tab_id="comparativa")
                                ],
                                id="tab_products",
                                active_tab="gasoline_95E5",
                                style=
                                    {
                                        "text-align":"center",
                                        "width": "100%",
                                        "margin-top": "1%",
                                        "font-size": "80%",
                                    }
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dcc.Dropdown(
                                    id="cluster-dd",
                                    options=["Todos"],
                                    value='Todos',
                                    clearable=False,
                                ),
                                width={"size": 2, "offset":10}
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                html.Div(
                                    id='divPlotMap',
                                    children=
                                        [
                                            html.H3("Mapas"),
                                            dbc.Card(
                                                [
                                                    dbc.Row(
                                                        dbc.Tabs(
                                                            [
                                                                dbc.Tab(label="Densidad",      tab_id="id_Densidad"),
                                                                dbc.Tab(label="Precio",        tab_id="id_Precio"),
                                                                dbc.Tab(label="Localizacion",  tab_id="id_Localizacion"),
                                                            ],
                                                            id="tab_mapas",
                                                            active_tab="id_Densidad",
                                                            style=
                                                                {
                                                                    "text-align":"center",
                                                                    "width": "100%",
                                                                    "margin-top": "1%",
                                                                    "font-size": "80%",
                                                                }
                                                        )

                                                    ),
                                                    dbc.Row(
                                                        dbc.CardBody(
                                                            [
                                                                    dcc.Graph(id="plotMap",
                                                                          figure=getMapa("id_Densidad", "gasoline_95E5", 'Todos', min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                                          style={'width': '100%', 'height': '100%'}),
                                                            ]
                                                        ),
                                                    )
                                                ],
                                                class_name='border-0'
                                            ),
                                        ]
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                         id='divPlotPie',
                                         children=
                                              [
                                                  html.H3("Cuota del total de gasolineras por empresa"),
                                                  dbc.Card(
                                                      dbc.CardBody([
                                                          dcc.Graph(id="plotPie",
                                                                    figure=getPie("gasoline_95E5", 'Todos', min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                                    style={'width': '100%', 'height': '100%'}
                                                                    )
                                                      ]),
                                                      class_name='border-0'
                                                  ),
                                              ]
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        id='divPlotPieCluster',
                                        children=
                                        [
                                            html.H3("Cuota del total de gasolineras por perfil"),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    dcc.Graph(id="plotPieCluster",
                                                              figure=getPieCluster("gasoline_95E5", 'Todos',
                                                                            min(df_parsed_1['date']),
                                                                            max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                              style={'width': '100%', 'height': '100%'}
                                                              )
                                                ]),
                                                class_name='border-0'
                                            ),

                                        ]
                                    )
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotViolinEmpresas',
                                children=
                                     [
                                         html.H3("Distribuci??n del precio"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph(id="plotViolinEmpresas",
                                                           figure=getViolinEmpresas("gasoline_95E5", 'Todos',  min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                           style={'width': '100%', 'height': '100%'}
                                                           )
                                             ]),
                                             class_name='border-0'
                                         ),
                                     ]
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotLineas',
                                children=
                                     [
                                         html.H3("Evoluci??n del precio"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph
                                                    (
                                                        id="plotLineas",
                                                        figure=getLineas("gasoline_95E5", 'Todos',  min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                        style={'width': '100%', 'height': '100%'}
                                                    )
                                             ]),
                                             class_name='border-0'
                                         ),
                                     ]
                            )
                        ),
                        html.Br(),
                        html.Br(),
                        html.Hr(),
                        html.Hr(),
                        html.Hr(),
                        html.Br(),
                        html.Br(),
                        dbc.Row(
                            html.Div(
                                id='divPlotForecast',
                                children=
                                     [
                                         html.H3("Forecasting con precio ajustado"),
                                         dbc.Card(
                                             dbc.CardBody([
                                                 dcc.Graph
                                                    (
                                                        id="plotForecast",
                                                        figure=getLineas("gasoline_95E5", 'Todos',  min(df_parsed_1['date']), max(df_parsed_1['date']), 'Todos', 'Todos'),
                                                        style={'width': '100%', 'height': '100%'}
                                                    )
                                             ]),
                                             class_name='border-0'
                                         ),
                                     ]
                            )
                        )
                    ],
                    style=
                        {
                            "text-align":"center",
                            "width": "100%",
                        }
                )
            ]
        ),
        html.Br(),

    ],
    fluid=True
)







####################### CALLBACKS

@app.callback( #Mapa a mostrar
    Output("plotMap", "figure"),
    Output("plotPie", "figure"),
    Output("plotPieCluster", "figure"),
    Output("plotViolinEmpresas", "figure"),
    Output("plotLineas", "figure"),
    Output("plotForecast", "figure"),
    Input("tab_mapas", 'active_tab'),
    Input("tab_products", 'active_tab'),
    Input("district-dd", 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input("barrio-dd", 'value'),
    Input("cluster-dd", 'value'),
)
def selectTabMap(active_tab_map, active_tab_prod, distrito, start_date, end_date, barrio, cluster):
    """
    Parameters:
    active_tab_map: str. identificador del tipo de mapa a representar (densidad, precio, localizacion)
    active_tab_prod: str. identificador del tipo de combustible a representar
    distrito: str. identificador del distrito a filtrar
    start_date: datetime. fecha de inicio del filtro
    end_date: datetime. fecha de fin del filtro
    barrio: str. nombre del barrio a filtrar
    cluster: str. nombre del cluster

    Output:
    fig: Figure. Grafica MapBox a representar
    fig: Figure. Piechart de cuota del total de las gasolineras a representar
    fig: Figure. Piechart del distribucion de las gasolineras por cluster
    fig: Figure. Grafica de violin a representar
    fig: Figure. Grafica de lineas a representar
    fig: Figure. Grafica de lineas con forecasting a representar
    """


    return [getMapa(active_tab_map, active_tab_prod, distrito, start_date, end_date, barrio, cluster),
            getPie(active_tab_prod, distrito, start_date, end_date, barrio, cluster),
            getPieCluster(active_tab_prod, distrito, start_date, end_date, barrio, cluster),
            getViolinEmpresas(active_tab_prod, distrito, start_date, end_date, barrio, cluster),
            getLineas(active_tab_prod, distrito, start_date, end_date, barrio, cluster),
            getForecast(active_tab_prod, distrito, start_date, end_date, barrio, cluster)]

@app.callback( # Barrios por distrito dd
    Output("barrio-dd", "options"),
    Input("district-dd", 'value'),
)
def barriosDeDistrito(distrito):
    """
    Asignacion de las opciones del dropdown de barrios en funcion del distrito

    Parameters:
    distrito: str. identificador del distrito

    Output:
    lista: list. barrios pertenecientes al distrito seleccionado
    """

    if distrito != 'Todos':
        return dictionaries.dict_district_neigh[distrito]
    else:
        return ["Todos"]

@app.callback( # Barrios por distrito dd
    Output("barrio-dd", "value"),
    Input("district-dd", 'value'),
    Input("barrio-dd", 'value')
)
def barriosDeDistritoDefecto(distrito, barrio):
    """
    Callback para resolver casos en los que el se cambia el distrito una vez se tenia un barrio seleccionado

    Parameters:
    distrito: str. identificador del distrito
    barrio: str. identificador del barrio

    Output:
    str: barrios pertenecientes al distrito seleccionado
    """

    if distrito == 'Todos':
        return "Todos"
    if barrio not in dict_district_neigh[distrito]:
        return "Todos"
    else:
        return barrio


@app.callback( # Barrios por distrito dd
    Output("cluster-dd", "options"),
    Input("tab_products", 'active_tab'),
)
def clustersDeProducto(producto):
    """
    Asignacion de las opciones del dropdown de cluster en funcion del producto

    Parameters:
    producto: str. identificador del producto

    Output:
    lista: list. clusters pertenecientes al producto seleccionado
    """

    return ["Todos"]+dict_products_clusters[producto]

@app.callback( # Barrios por distrito dd
    Output("cluster-dd", "value"),
    Input("tab_products", 'active_tab'),
)
def clustersDeProductoDefecto(producto):
    """
    Callback para resolver casos en los que el se cambia el producto y ya  se tenia un cluster seleccionado

    Output:
    str: barrios pertenecientes al distrito seleccionado
    """
    return "Todos"



if __name__ == "__main__":
    app.title = "GeoPortal"
    app.config.suppress_callback_exceptions = False
    app.run_server(debug=True, port=8080)




