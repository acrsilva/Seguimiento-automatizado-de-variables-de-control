# -*- coding: utf-8 -*-

"""

Esto es una prueba de un gráfico de barras mostrando 1024 datos aleatorios

"""


import pyqtgraph as pg
from PyQt4 import QtGui
import sys
import numpy as np


n = 1024  # number of rectangles for BarGraphItem


def onViewRangeChanged(viewRange, x, y, barGraphItem):
    """Updates barGraphItem data depending on plotItem viewRange.
    @param viewRange: PlotItem viewRange
    @param x, y: Data of barGraphItem
    @param barGraphItem: BarGraphItem which data is to be updated
    """
    v = list()
    v.append(max(x[0], viewRange[0]))
    v.append(min(x[-1], viewRange[-1]))
    # n = 1024
    newX = np.linspace(v[0], v[1], n)
    newY = np.interp(newX, x, y)
    # colors must be interpolated either in my task, here I just create new list of random colors
    colors = [pg.intColor(np.random.randint(1, 100)) for i in xrange(n)]
    barGraphItem.setOpts(x0=newX[:-1], x1=newX[1:], y0=[0] * n, y1=newY, brushes=colors, pens=colors)


app = QtGui.QApplication(sys.argv)
view = pg.GraphicsView()
plt = pg.PlotItem()
plt.getViewBox().setMouseEnabled(True, False)
view.setCentralItem(plt)

# ---------data for barGraphItem-----------
# initial x and y
x = np.arange(6040, 7270, 0.1)
y = np.cos(x)
# normalized y
y = (y - min(y)) / (max(y) - min(y))
# split curve in n=1024 intervals
xGrid = np.linspace(x[0], x[-1], n)
yGrid = np.interp(xGrid, x, y)
colors = [pg.intColor(np.random.randint(1, 100)) for i in xrange(n)]
#colors = [pg.intColor(1) for i in xrange(n)]

barGraphItem = pg.BarGraphItem()
barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, y1=0.3, brushes=colors, pens=colors)

plt.addItem(barGraphItem)

#plt.getViewBox().sigRangeChanged.connect(lambda: onViewRangeChanged(plt.getViewBox().viewRange()[0], x, y, barGraphItem))

view.show()
app.exec_()
