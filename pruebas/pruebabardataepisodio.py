# -*- coding: utf-8 -*-

"""

Prueba de gráfico de barras mostrando un episodio de sueño

"""


import pyqtgraph as pg
from PyQt4 import QtGui
import sys
import numpy as np

app = QtGui.QApplication(sys.argv)
view = pg.GraphicsView()
plt = pg.PlotItem()
plt.getViewBox().setMouseEnabled(True, False)
view.setCentralItem(plt)

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
x = csv[:,1]
y = csv[:,25]

#Trocear datos en episodios
a = -1
b = -1
c = 0
for i in range(len(y)):
	if(y[i] != 0 and a == -1): #dormido
		a = i #comienzo del episodio
	elif(y[i] == 0 and a != -1 and b < 100): #despierto
		b = b + 1
	elif(b >= 100 and c == 0):
		c = 1
		b = i #fin del episodio
	k = i
print "a:%i b:%i k:%i\n" %(a, b, k)

#Elegir episodio a mostrar
n = b-a
x = x[a:b]
y = y[a:b]
xGrid = np.linspace(x[0], x[-1], n)
yGrid = np.interp(xGrid, x, y)

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

barGraphItem = pg.BarGraphItem()
#barGraphItem = pg.BarGraphItem(x=x[a:b], height=0.3, width=1, brushes=colors[a:b], pens=colors[a:b]) #No se ven las verdes
barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=0.3, brushes=colors, pens=colors)
plt.addItem(barGraphItem)

#Cambios de episodios
#plt.getViewBox().sigRangeChanged.connect(lambda: onViewRangeChanged(plt.getViewBox().viewRange()[0], x, y, barGraphItem))

view.show()
app.exec_()
