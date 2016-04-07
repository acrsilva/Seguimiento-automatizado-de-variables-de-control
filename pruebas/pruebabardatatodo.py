# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PyQt4 import QtGui
import sys
import numpy as np

app = QtGui.QApplication(sys.argv)
view = pg.GraphicsView()
plt = pg.PlotItem()
plt.getViewBox().setMouseEnabled(True, False)
view.setCentralItem(plt)

# split curve in n=1024 intervals
#xGrid = np.linspace(x[0], x[-1], n)
#yGrid = np.interp(xGrid, x, y)

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
x = csv[:,1]
y = csv[:,25]
n = len(x) #nº de barras a dibujar
#print "x:%i y:%i\n" % (len(x), len(y))
xGrid = np.linspace(x[-1], x[0], n)
yGrid = np.interp(xGrid, x, y)
#print "x:%i y:%i\n" % (len(xGrid), len(yGrid))

colors = []
num = 0
for i in y:
	if(i == 2): #Sueño ligero - Naranja
		c = pg.mkColor(255, 128, 0)
	elif(i == 4): #Sueño profundo - Amarillo
		c = pg.mkColor(255, 255, 0)
	elif(i == 5): #Sueño muy profundo - Verde
		c = pg.mkColor(0, 255, 0)
		#print "Verde! en %i\n" % num
	else: #Despierto - Rojo
		c = pg.mkColor(255, 0, 0)
	colors.append(c)
	num = num + 1
#print "num = %i\n" % num	
#print "colores: %i\n" % len(colors)

barGraphItem = pg.BarGraphItem()
#barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, y1=0.3, brushes=colors, pens=colors)
barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=0.3, brushes=colors, pens=colors)
plt.addItem(barGraphItem)

#plt.getViewBox().sigRangeChanged.connect(lambda: onViewRangeChanged(plt.getViewBox().viewRange()[0], x, y, barGraphItem))

view.show()
app.exec_()
