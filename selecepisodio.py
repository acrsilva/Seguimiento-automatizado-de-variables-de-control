# -*- coding: utf-8 -*-

"""
v.02
Gestiona los episodios de sueño desde un fichero de datos
Permite obtener gráficos de barras para cada episodio de sueño
y para cada episodio de consumo energético

Columnas: 1.tiempo, 17.consumo energético, 24. clasif actividad, 25.clasif sueño
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
import datetime

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
tiempos = csv[:,0] / (1000) #Tiempo en minutos
suenos = csv[:,25] #Clasificador de sueño
#actividades = csv[:,24] #Clasificador de actividad 1, 2, 3, 4, 5, 7, 9
consumos = csv[:,24] #Consumo energético


rango = 6 * 60 #6 horas

def cargarActividad():
    sedentaria = csv[:,18]
    ligera = csv[:,19]
    moderada = csv[:,20]
    
    actividad = []
    for i in range(len(tiempos)):
        if(sedentaria[i]):
            actividad.append(0)
        elif(ligera[i]):
            actividad.append(1)
        elif(moderada[i]):
            actividad.append(2)
        else:
            print "error de actividad"
            actividad.append(-1)
        print actividad[i]
    return actividad
    print "%i actividades" % len(actividad)

def trocear(y):
    print "troceando, num y: %i" % len(suenos)
    indices = []
    a = False
    c = 0
    t = 0
    f = 0
    for i in range(len(suenos)):
        if(not a and suenos[i] != 0): #nuevo episodio
            c = i 
            a = True
            f = i
        elif(a): #episodio comenzado
            if(suenos[i] !=0): #dormido(resetear tiempo despierto)
                t = 0
                f = i
            elif(t < 60): #despierto(cuanto tiempo?)
                t = t + 1
            else: #fin del episodio (1h seguida despierto)
                indices.append([c, f])
                t = 0
                a = False
                c = 0
                f = 0
    return indices

def coloreaSueno():
	print "coloreando barras de sueño"
	colors = []
	num = 0
	for i in suenos:
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
    
def coloreaActividades():
    print "coloreando barras de actividad fisica"
    colors = []
    num = 0
    for i in actividades:
        if(i == 0):
            c = pg.mkColor(255, 51, 51)
        if(i == 1):
            c = pg.mkColor(102, 255, 102)
        elif(i == 2):
            c = pg.mkColor(0, 102, 0)
        else:
            c = pg.mkColor(255, 0, 0)  
            print "ninguna"  
        colors.append(c)
        num = num + 1
    print "num colores de actividades %i" % len(colors)
    return colors

def imprimeIndicesEp(indices):
	print "Imprimiendo indices..."
	k = 0
	for i in indices:
		print "indice %i : %i - %i" % (k, i[0], i[1]) 
		k = k+1
	

def creaConsumoData(ep, indices):
    print "creando grafica de consumo energético"
    """
    if(indices[ep][0] - (3 * 60) < 0):
        a = 0
    else:    
        a = indices[ep][0] - (3 * 60)
    """   
    a = indices[ep][0] - rango
    b = indices[ep][1] + rango
    n = b-a
    print "rango consumo: %i a:%i b:%i" % (n, a, b)
    return actividades[a:b]

"""
Crea una barra de colores con la clasificación del sueño de un episodio de sueño
y la clasificación de actividades durante varias horas antes y después del episodio
"""
def creaBarra(ep, ind, cs, ca):
    #comienzo y final del episodio de sueño
    eini = ind[ep][0]
    efin = ind[ep][1]
    #comienzo y final del episodio completo
    ini = eini - rango
    fin = efin + rango
    #Longitud del episodio completo
    n = fin - ini
    
    colors = []
    colors.extend(ca[ini:eini])
    colors.extend(cs[eini:efin])
    colors.extend(ca[efin:fin])
    
    print colors[0]
    print "%i colores en barra" % len(colors)
    print "n %i ini %i eini %i efin %i fin %i tiempos: %i" % (n, ini, eini, efin, fin, len(tiempos[ini:fin]))
    
    barra = pg.BarGraphItem(x0=(tiempos[ini:fin]), width=60, height=1, brushes=colors, pens=colors)
    
    return barra

actividades = cargarActividad()
class SelecEpisodio(object):
    #Obtener indices de cada episodio de todo el intervalo de sueño
    indices = trocear(suenos)
    imprimeIndicesEp(indices)
    colorsuenos = coloreaSueno()
    coloracts = coloreaActividades()

    #Elegir el episodio inicial
    epAct = 0
    barraSuenio = creaBarra(epAct, indices, colorsuenos, coloracts)
    consumoData = creaConsumoData(epAct, indices)
    horas = tiempos[indices[epAct][0] - rango : indices[epAct][1] + rango]

    print datetime.datetime.fromtimestamp(horas[0])
    
    
    def episodioSiguiente(cls):
        if (cls.epAct < len(cls.indices) - 1): #Último episodio
            cls.epAct += 1
            print "siguiente episodio: %i" % cls.epAct
            cls.barraSuenio = creaBarra(cls.epAct, cls.indices, cls.colorsuenos, cls.coloracts)
            cls.consumoData = creaConsumoData(cls.epAct, cls.indices)
            #Establecer el rango nuevo
            

    def episodioAnterior(cls):
        if (cls.epAct > 0): #Primer episodio
            cls.epAct -= 1
            print "anterior episodio: %i" % cls.epAct
            cls.barraSuenio = creaBarra(cls.epAct, cls.indices, cls.colorsuenos, cls.coloracts)
            cls.consumoData = creaConsumoData(cls.epAct, cls.indices)
        


		
