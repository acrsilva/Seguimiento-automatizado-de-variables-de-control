# -*- coding: utf-8 -*-

"""

Gestiona los episodios de sueño desde un fichero de datos
Permite obtener gráficos de barras para cada episodio de sueño
y para cada episodio de consumo energético

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
x = csv[:,1]
y = csv[:,25]

def trocear(y):
	print "troceando, num y: %i" % len(y)
	indices = []
	a = False
	c = 0
	f = 0
	for i in range(len(y)):
		if(not a and y[i] != 0): #nuevo episodio
			c = i 
			a = True
		elif(a): #dormido->despierto
			if(y[i] !=0): #dormido(resetear tiempo despierto)
				f = 0
			else: #despierto(cuanto tiempo?)
				if(f < 60):
					f = f + 1
				else: #fin del episodio (1h seguida despierto)
					f = i
					indices.append([c, f])
					a = False
					c = 0
					f = 0
	return indices

def colorea():
	print "coloreando"
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
	print "num colores %i" % len(colors)	
	return colors	

def imprimeIndicesEp(indices):
	print "Imprimiendo indices..."
	k = 0
	for i in indices:
		print "indice %i : %i - %i" % (k, i[0], i[1]) 
		k = k+1
	

class SelecEpisodio(object):
	#Obtener indices de cada episodio de todo el intervalo de sueño
	indices = trocear(y)
	
	imprimeIndicesEp(indices)
	
	colors = colorea()
		
	#Elegir episodio a mostrar
	a = indices[0][0]
	b = indices[0][1]
	n = b-a
	xp = x[a:b]
	yp = y[a:b]
	xGrid = np.linspace(xp[0], xp[-1], n)
	yGrid = np.interp(xGrid, xp, yp)	
	
		
	barGraphItem = pg.BarGraphItem()
	barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=1, brushes=colors[a:b], pens=colors[a:b])
	
	consumoBar = pg.BarGraphItem()
	consumoBar.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=1, brushes=colors, pens=colors)

	def episodioSiguiente(cls):
		print "hola"
		
	#def episodioAnterior(cls):	
		
	def getSuenioBar(cls):
		return cls.barGraphItem
	
	def getConsumoBar(cls):
		return cls.barConsumo
		
	def getX(cls):
		return x	

		
