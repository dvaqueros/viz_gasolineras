import plotly.express as px
from dictionaries import *
import plotly.graph_objects as go
import pickle



def crearForecast(df_lineas, product):
    with open("data/output/modelos", 'rb') as f:
        modelos = pickle.load(f)

    df_prediccion=modelos[product]['Cluster 0']['model'].predict(steps=30)

    fig = go.Figure()
    if len(df_lineas):
        #print(product)
        #print(df_lineas)
        # Realizamos una media por fecha del precio del combustible en todas las gasolineras.
        #df_lineas = df_lineas.groupby(['date'], group_keys=True).mean().reset_index()
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
                      #title='Serie temporal del precio de ' + product
                      )
        fig.add_trace(
            px.line(df_prediccion,
                    #x='date',
                    y='pred',
                    color_discrete_sequence=[palette[5]],
                    labels={
                        "value": "Precio medio (€)",
                        "date": "Fecha",
                        "variable": "Combustible"
                    },
                    # title='Serie temporal del precio de ' + product
                    ).data[0])

        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")

    return fig