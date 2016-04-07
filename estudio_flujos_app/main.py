# -*- coding: utf-8 -*-

import cachitos
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

# some setting for this notebook to actually show the graphs inline, you probably won't need this
np.set_printoptions(precision=5, suppress=True)  # suppress scientific float notation

episodio = 0
sel = cachitos.selEpisodio("../data.csv")
csv = sel.epFiltro
print "total episodios: ", len(csv)

sel.filSueno = True
sel.filSedentario = False
sel.filLigero = False
sel.filModerado = False
sel.update()
csv = sel.epFiltro
print "episodios de sueño: ", len(csv)


X = np.zeros(shape=(0,2))
for i in csv:
    x = np.c_[i.temp, i.flujo]
    X = np.concatenate((X,x),)
    
print X.shape

#plt.scatter(X[:,0], X[:,1])
#plt.show()

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
Z = linkage(X, 'centroid')


c, coph_dists = cophenet(Z, pdist(X))

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
