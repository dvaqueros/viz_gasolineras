

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

#
with open("data/output/dict_df_products_clustering", 'rb') as f:
    dict_df_products_clustering = pickle.load(f)

with open("data/output/diccionario_df_productos", 'rb') as f:
    dict_df_products= pickle.load(f)

dict_df_products_clustering_2 = {}
for producto in products:
    df_original = dict_df_products[producto]
    df_clustering = dict_df_products_clustering[producto]
    dict_df_products_clustering_2[producto]=df_original[['station_id', 'date']+columnas_clust_drop].merge(df_clustering, left_on=['station_id', 'date'], right_on=['station_id', 'date'], how='left', suffixes=('', '_y'))#.drop(columns='Series')

pickle.dump(dict_df_products_clustering_2, open("data/output/dict_df_products_clustering_2", "wb"))
