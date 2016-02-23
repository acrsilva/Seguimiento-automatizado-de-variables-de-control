# -*- coding: utf-8 -*-

"""

Prueba para insertar la prueba de gráfico de barras con episodio de sueño
utilizando Qt designer y generando el código dinámicamente, es decir, sin 
compilar previamente

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os

pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'intbarras.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class MainWindow(TemplateBaseClass):  
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        #self.ui.plotBtn.clicked.connect(self.plot)
        
        plt = pg.PlotItem()
        plt.getViewBox().setMouseEnabled(False, False)
        self.ui.graphicsView.setCentralItem(plt)
        plt.addItem(barGraphItem)
        
        self.show()
        
    def plot(self):
        self.ui.plot.plot(np.random.normal(size=100), clear=True)
        

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
barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=1, brushes=colors, pens=colors)

win = MainWindow()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
