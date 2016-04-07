# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
csv = sel.epFiltro[episodio]
print len(csv)


sel.filSueno = True
sel.filSedentario = False
sel.filLigero = False
sel.filModerado = False
sel.update()
csv = sel.epFiltro[episodio]
print len(csv)

X = np.c_[csv.temp, csv.flujo]
print X.shape

#plt.scatter(X[:,0], X[:,1])
#plt.show()

Z = linkage(X)


c, coph_dists = cophenet(Z, pdist(X))

print c, Z[0]



