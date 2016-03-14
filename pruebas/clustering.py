# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist


csv = np.genfromtxt ('data.csv', delimiter=",")
a = csv[:,8]
b = csv[:,26]
X = np.c_[a,b]

print X.shape 
plt.scatter(X[:,0], X[:,1])
plt.show()

Z = linkage(X, 'ward')

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



print "Fin"

