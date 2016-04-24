"""
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist


csv = np.genfromtxt ('../data.csv', delimiter=",")
a = csv[:300,8]
b = csv[:300,26]
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

"""

import scipy
import scipy.cluster.hierarchy as sch
import matplotlib.pylab as plt

n=10
k=3
X = scipy.randn(n,2)
d = sch.distance.pdist(X)
Z= sch.linkage(d,method='complete')
T = sch.fcluster(Z, k, 'maxclust')

print "X: ", X
print "d " , d

# calculate labels
labels=list('' for i in range(n))
for i in range(n):
    labels[i]=str(i)+ ',' + str(T[i])

# calculate color threshold
ct=Z[-(k-1),2]  

#plot
P =sch.dendrogram(Z,labels=labels,color_threshold=ct)
plt.show()
