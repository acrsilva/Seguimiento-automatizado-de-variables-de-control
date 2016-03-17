# -*- coding: utf-8 -*-

"""
v.01
Gestiona los episodios de sueño desde un fichero de datos
Permite obtener gráficos de barras para cada episodio de sueño
y para cada episodio de consumo energético

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
x = csv[:,1] #Tiempo
y = csv[:,25] #Clasificador de sueño
z = csv[:,24] #Clasificador de actividad 1, 2, 3, 4, 5, 7, 9
k = csv[:,24] #Consumo energético

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
            elif(f < 60): #despierto(cuanto tiempo?)
                f = f + 1
            else: #fin del episodio (1h seguida despierto)
                f = i
                indices.append([c, f])
                a = False
                c = 0
                f = 0
    return indices

def coloreaSueno():
	print "coloreando barras de sueño"
	colors = []
	num = 0
	for i in y:
		if(i == 2): #Sueño ligero
			c = pg.mkColor(102, 102, 255)
		elif(i == 4): #Sueño profundo
			c = pg.mkColor(0, 0, 204)
		elif(i == 5): #Sueño muy profundo
			c = pg.mkColor(0, 0, 102)
		else: #Despierto
			c = pg.mkColor(255, 255, 0)
		colors.append(c)
		num = num + 1
	print "num colores %i" % len(colors)	
	return colors
    
def coloreaConsumo():
    print "coloreando barras de actividad fisica"
    colors = []
    num = 0
    for i in z:
        if(i == 1):
            c = pg.mkColor(255, 51, 51)
        elif(i == 2):
            c = pg.mkColor(204, 255, 204)
        elif(i == 3):
            c = pg.mkColor(102, 255, 102)
        elif(i == 4):
            c = pg.mkColor(0, 255, 0)
        elif(i == 5):
            c = pg.mkColor(0, 204, 0)
        elif(i == 7):
            c = pg.mkColor(0, 153, 0)    
        elif(i==9):
            c = pg.mkColor(0, 102, 0)
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
	
def creaSuenoBar(ep, indices, colors):
	a = indices[ep][0]
	b = indices[ep][1]
	n = b-a
	xp = x[a:b]
	yp = y[a:b]
	xGrid = np.linspace(xp[0], xp[-1], n)
	yGrid = np.interp(xGrid, xp, yp)	
	barGraphItem = pg.BarGraphItem()
	barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=1, brushes=colors[a:b], pens=colors[a:b])
	return barGraphItem
	
def creaActividadBar(ep, indices, colors):
    #if(indices[ep][0] - (3 * 60) < 0):
        #a = 0
    #else:    
        #a = indices[ep][0] - (3 * 60)
    a = indices[ep][0] - (3 * 60)    
    b = indices[ep][1]
    n = b-a
    print "rango actividad: %i" % n
    xp = x[a:b]
    zp = z[a:b]
    xGrid = np.linspace(xp[0], xp[-1], n)
    zGrid = np.interp(xGrid, xp, zp)	
    barGraphItem = pg.BarGraphItem()
    barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=0.5, brushes=colors[a:b], pens=colors[a:b])
    return barGraphItem

def creaConsumoData(ep, indices):
    print "creando grafica de consumo energético"
    """
    if(indices[ep][0] - (3 * 60) < 0):
        a = 0
    else:    
        a = indices[ep][0] - (3 * 60)
    """   
    a = indices[ep][0] - (3 * 60) 
    b = indices[ep][1]
    n = b-a
    print "rango consumo: %i" % n
    return k[a:b]
    

class SelecEpisodio(object):
    #Obtener indices de cada episodio de todo el intervalo de sueño
    indices = trocear(y)
    imprimeIndicesEp(indices)
    colors = coloreaSueno()
    consColors = coloreaConsumo()

    #Elegir el episodio inicial
    epAct = 0
    barSuenio = creaSuenoBar(epAct, indices, colors)
    barConsumo = creaActividadBar(epAct, indices, consColors)
    consumoData = creaConsumoData(epAct, indices)
    
    def episodioSiguiente(cls):
        if (cls.epAct < len(cls.indices) - 1): #Último episodio
            cls.epAct += 1
            cls.barSuenio = creaSuenoBar(cls.epAct, cls.indices, cls.colors)
            cls.barConsumo = creaActividadBar(cls.epAct, cls.indices, cls.consColors)
            cls.consumoData = creaConsumoData(cls.epAct, cls.indices)
        print "siguiente episodio: %i" % cls.epAct

    def episodioAnterior(cls):
        if (cls.epAct > 0): #Primer episodio
            cls.epAct -= 1
            cls.barSuenio = creaSuenoBar(cls.epAct, cls.indices, cls.colors)
            cls.barConsumo = creaActividadBar(cls.epAct, cls.indices, cls.consColors)
            cls.consumoData = creaConsumoData(cls.epAct, cls.indices)
        print "anterior episodio: %i" % cls.epAct


		
