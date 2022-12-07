# Inspirado por https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering/notebook

# Native libraries
import os
import math
# Essential Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Preprocessing
from sklearn.preprocessing import MinMaxScaler
# Algorithms
from minisom import MiniSom
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans

# Para un eficiente funcionamiento de los bucles utilizados para guardar los binarios se ha comentado las lineas de
# output y pasos intermedios del entrenamiento.


columnas_clust_drop = [
    'name',
    'address',
    'zip_code',
    'road_side',
    'restriction',
    'sender',
    'schedule',
    'vivienda_agua_electricidad_combustibles',
    'min_distance',
    'district',
    'neighbourhood',
    'schedule_parsed',
    'name_parsed',
    'num_combustibles'
]

dict_df_products_clustering = dict_df_products.copy()
for producto in products:
    dict_df_products_clustering[producto]=dict_df_products_clustering[producto].drop(columns=columnas_clust_drop)


for producto in products:
    #print(producto)
    mySeries = []
    namesOfMySeries = []
    for station in dict_df_products_clustering[producto]['station_id'].unique():
        #print(station)
        df = dict_df_products_clustering[producto][dict_df_products_clustering[producto]['station_id']==station]
        df = df.loc[:, [producto]]


        mySeries.append(df.to_numpy().transpose()[0])
        namesOfMySeries.append(station)

    som_x = som_y = math.ceil(math.sqrt(math.sqrt(len(mySeries))))

    som = MiniSom(som_x, som_y, len(mySeries[0]), sigma=0.3, learning_rate=0.1)

    som.random_weights_init(mySeries)
    som.train(mySeries, 50000)


    win_map = som.win_map(mySeries)



    win_map = som.win_map(mySeries)



    cluster_map = []
    for idx in range(len(mySeries)):
        winner_node = som.winner(mySeries[idx])
        cluster_map.append((namesOfMySeries[idx], f"Cluster {winner_node[0] * som_y + winner_node[1] + 1}"))

    df_som = pd.DataFrame(cluster_map, columns=["Series", "Cluster"]).sort_values(by="Cluster").set_index("Series").reset_index()








    cluster_count = math.ceil(math.sqrt(len(mySeries)))

    km = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    labels = km.fit_predict(mySeries)

    plot_count = math.ceil(math.sqrt(cluster_count))




    plot_count = math.ceil(math.sqrt(cluster_count))


    fancy_names_for_labels = [f"Cluster {label}" for label in labels]
    df_kmeans = pd.DataFrame(zip(namesOfMySeries, fancy_names_for_labels), columns=["Series", "Cluster"]).sort_values(
        by="Cluster").set_index("Series").reset_index()


    df_original=dict_df_products_clustering[producto]
    dict_df_products_clustering[producto] = df_original.merge(df_som, left_on='station_id', right_on='Series', how='left').drop(columns='Series')
    dict_df_products_clustering[producto] = df_original.merge(df_kmeans, left_on='station_id', right_on='Series', how='left', suffixes=('_som', '_kmeans')).drop(columns='Series')

pickle.dump(dict_df_products_clustering, open("data/output/dict_df_products_clustering", "wb"))