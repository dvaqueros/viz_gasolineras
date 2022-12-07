import plotly.express as px
from dictionaries import *
import plotly.graph_objects as go
import pickle

def crearForecast(df_lineas, product, cluster):
    """
    Parameters:
    df_lineas: df. dataframe con el conjunto de datos ya filtrado
    product: str. combustible del que se realiza la visualizacion
    cluster: str. cluster del que se realiza la visualizacion

    Output:
    fig: Figure. grafico con la represntacion temporal de los datos y una prediccion de esta.
    """

    fig = go.Figure()

    if cluster!='Todos':
        with open("data/output/modelos", 'rb') as f:
            modelos = pickle.load(f)

        df_prediccion=modelos[product][cluster]['model'].predict(steps=18)

        if len(df_lineas):
            # Realizamos una media por fecha del precio del combustible en todas las gasolineras.
            df_lineas = df_lineas.groupby(['date'], as_index=False).agg({product+'_adj': 'mean'}).reset_index()

            fig = px.line(df_lineas,
                          x='date',
                          y=[product+'_adj'],
                          color_discrete_sequence=[palette[0]],
                          labels={
                              "value": "Precio medio (€)",
                              "date": "Fecha",
                              "variable": "Combustible"
                          },
                          )
            fig.add_trace(
                px.line(df_prediccion,
                        y='pred',
                        color_discrete_sequence=[palette[5]],
                        labels={
                            "value": "Precio medio (€)",
                            "date": "Fecha",
                            "variable": "Combustible"
                        },
                        ).data[0])

            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x")

    return fig