# -*- coding: utf-8 -*-

import sys
import cachitos
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from sklearn import preprocessing
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import scipy.spatial.distance as ssd
import math


class Individuo:
    def __init__(self, tiempo, temperatura, flujo):
        self.tiempo = tiempo
        self.stt = temperatura
        self.stf = flujo


#np.set_printoptions(precision=5, suppress=True)

sel = cachitos.selEpisodio("../data.csv")

sel.filSueno = True
sel.filSedentario = False
sel.filLigero = False
sel.filModerado = False
sel.update()
# Obtener los episodios de sueño del fichero
csv_sueno = sel.epFiltro
print "episodios de sueño: ", len(csv_sueno)

# Normalizar los episodios de sueño
eps_sueno = []
for i in csv_sueno:
    #Normalizar temperatura y flujo
    a = preprocessing.scale(i.temp, copy=False)
    b = preprocessing.scale(i.flujo, copy=False)
    eps_sueno.append(Individuo(i.tiempo, a, b))


#Calcular distancias
s = len(eps_sueno)
distancias = np.zeros((s, s)) #Matriz de distancias entre individuos

"""
#La diagonal de distancias no da 0, mismas ST dan distancias >0 !!!
for i in range(s):
    print eps_sueno[i].stt[-1], eps_sueno[i].stt[-1]

for i in range(s):
    d, p = fastdtw(eps_sueno[i].stt, eps_sueno[i].stt, dist=euclidean)
    dd, p = fastdtw(eps_sueno[i].stf, eps_sueno[i].stf, dist=euclidean)
    print d, dd
"""

for i in range(s):
    for j in range(s):
        if(i != j):
            distanceTemp , path = fastdtw(eps_sueno[i].stt, eps_sueno[j].stt, dist=euclidean) #Distancia en temperatura
            distanceFlujo , path = fastdtw(eps_sueno[i].stf, eps_sueno[j].stf, dist=euclidean) #Distancia en flujo
            distancias[j][i] = math.sqrt(math.pow(distanceTemp + distanceFlujo, 2)) #Distancia euclídea total

print "pruebas"

#Vector con las distancias requeridas para hacer clustering
print len(distancias), "distancias"
print distancias
print distancias.shape

"""
Resultados:
centroid: 0.82848866781
single: 0.340428699013
complete: 0.80537453305
average: 0.827708738138
weighted: 0.816403408353
median: 0.772500661416
ward: 0.823703775985
"""
dists = ssd.squareform(distancias)
Z = linkage(dists, 'average')


#c, coph_dists = cophenet(Z, pdist(X))
c, coph_dists = cophenet(Z, distancias)

print c


plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,
    leaf_font_size=8.,
)
plt.show()
