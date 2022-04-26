import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

#Se llaman los datasets 
movies_ds = pd.read_csv("movies.csv")
ratings_ds = pd.read_csv("ratings.csv.zip")

movies_ds = pd.read_csv("movies.csv")
ratings_ds = pd.read_csv("ratings.csv.zip")

#Mostar tabla rating
ratings_ds.head()
#Mostrar tabla peliculas
movies_ds.head()
#Se aplica la funcion pivot en el DataSet de rating para evitar la repeticion de datos
dataset_final = ratings_ds.pivot(index='movieId',columns='userId',values='rating')
dataset_final.head()
#Se usa la funcion fillna para rellenar de 0 la tabla y que no salgan NaN
dataset_final.fillna(0,inplace=True)
dataset_final.head()
#Se filtran los grupos por id de la pelicula y por el id del usuario basandose en la tabla de pivot
usarios_no_votaron = ratings_ds.groupby('movieId')['rating'].agg('count')
peliculas_no_votaro  = ratings_ds.groupby('userId')['rating'].agg('count')
#
usarios_no_votaron  = ratings_ds.groupby('movieId')['rating'].agg('count')
peliculas_no_votaro  = ratings_ds.groupby('userId')['rating'].agg('count')
#Se pone una restriccion para que las peliculas por las cuales votaron menos de 10 veces se filtren
dataset_final = dataset_final.loc[usarios_no_votaron[usarios_no_votaron > 10].index,:]
#Se pone una restriccion para que los por las cuales votaron menos de 50 veces se filtren
dataset_final=dataset_final.loc[:,peliculas_no_votaro[peliculas_no_votaro> 50].index]
dataset_final

#Se reduce el esparcimiento 
reduccion = np.array([[0,0,3,0,0],[4,0,0,0,2],[0,0,0,0,1]])
esp = 1.0 - ( np.count_nonzero(reduccion) / float(reduccion.size) )
print(esp)

muestra = csr_matrix(reduccion)
print(muestra)


datos = csr_matrix(dataset_final.values)
dataset_final.reset_index(inplace=True)

#Se implementa el coseno 
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(datos)
print(knn)

def obtener_recomendacion(titulo_pel):
    #Se revisa si la pelicula ingresada esta en el dataset
    #Se escoge solamente el top 10 de la peliculas a recomendar
    n_pel = 10
    lista_pelicula = movies_ds[movies_ds['title'].str.contains(titulo_pel)]  
    if len(lista_pelicula):        
        id_pel = lista_pelicula.iloc[0]['movieId']
        id_pel = dataset_final[dataset_final['movieId'] == id_pel].index[0]
        distancias , indices = knn.kneighbors(datos[id_pel],n_neighbors=n_pel+1)    
        recomendacion = sorted(list(zip(indices.squeeze().tolist(),distancias.squeeze().tolist())),\
                               key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        
        for val in recomendacion:
            id_pel = dataset_final.iloc[val[0]]['movieId']
            idx = movies_ds[movies_ds['movieId'] == id_pel].index
            recommend_frame.append({'Titulo':movies_ds.iloc[idx]['title'].values[0]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_pel+1))
        
        return df
    
    else:
        
        return "Ninguna pelicula encontrada"


'''get_movie_recommendation('Iron Man')'''

