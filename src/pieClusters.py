import plotly.express as px
from dictionaries import *
import plotly.graph_objects as go



def crearPieCluster(df):
    fig=go.Figure()
    if(len(df)):
        df_parsed=df
        last_date=max(df_parsed['date'])
        fig = px.pie(df_parsed[df_parsed['date'] == last_date],
                     values = 'station_id',
                     names = 'Cluster',
                     #title = 'Reparto de gasolineras por empresa',
                     color = 'Cluster',
                     labels = {'Cluster':'Perfil',
                            'station_id':'Gasolineras'},
                     color_discrete_map = colore_clusters)
        fig.update_traces(textposition='inside',
                          textinfo = 'percent+label',
                          showlegend=False)
    return fig