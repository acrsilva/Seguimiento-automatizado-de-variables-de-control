# -*- coding: utf-8 -*-

"""
v.02
Gestiona los episodios de sueño desde un fichero de datos
Permite obtener gráficos de barras para cada episodio de sueño
y para cada episodio de consumo energético

Columnas: (1)tiempo, (17)consumo energético, (25)clasif sueño
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
consumos = csv[:,17] #Consumo energético
temperaturas = csv[:,8] #Temperatura media (piel-4, 8-cuerpo)
flujos = csv[:,26] #Flujo térmico

rango = 6 * 60 #Horas antes y después del episodio de sueño

def cargarActividad():
    print "Cargando clasificación de actividad física"
    
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
            print "Error de actividad"
            actividad.append(0)
    return actividad

def trocear():
    print "Cargando índices de episodios de sueño"
    
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
	print "Coloreando sueños"
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
	return colors
    
def coloreaActividades():
    print "Coloreando clasificación de actividad física"
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
        colors.append(c)
        num = num + 1
    return colors

def imprimeIndicesEp(indices):
	print "Imprimiendo indices de episodios de sueño"
	k = 0
	for i in indices:
		print "indice %i : %i - %i" % (k, i[0], i[1]) 
		k = k+1
	

"""
Crea una barra de colores con la clasificación del sueño de un episodio de sueño
y la clasificación de actividades durante varias horas antes y después del episodio
"""
def creaBarra(ini, fin, eini, efin, cs, ca):
    print "Creando barra de colores"
    #Longitud del episodio completo
    n = fin - ini
    colors = []
    colors.extend(ca[ini:eini])
    colors.extend(cs[eini:efin])
    colors.extend(ca[efin:fin])
    
    print len(colors)
    print len(tiempos[ini:fin])
    
    return pg.BarGraphItem(x0=(tiempos[ini:fin]), width=60, height=1, brushes=colors, pens=colors)
    

def creaEpisodio(ep, ind, colorsuenos, coloracts):
    print "Creando episodio completo"
    #comienzo y final del episodio de sueño
    eini = ind[ep][0]
    efin = ind[ep][1]
    #comienzo y final del episodio completo
    ini = eini - rango
    fin = efin + rango
    if(ini < 0):
        ini = 0
    if(fin > len(tiempos)):
        fin = len(tiempos)-1
    
    barraSuenio = creaBarra(ini, fin, eini, efin+1, colorsuenos, coloracts)
    horas = tiempos[ini : fin]
    consumoData = consumos[ini:fin]
    flujoData = flujos[ini:fin]
    tempData = temperaturas[ini:fin]
    
    return barraSuenio, horas, consumoData, flujoData, tempData

actividades = cargarActividad()

class SelecEpisodio(object):
    #Obtener indices de cada episodio de todo el intervalo de sueño
    indices = trocear()
    imprimeIndicesEp(indices)
    colorsuenos = coloreaSueno()
    coloracts = coloreaActividades()

    #Elegir el episodio inicial
    epAct = 0
    barraSuenio, horas, consumoData, flujoData, tempData = creaEpisodio(epAct, indices, colorsuenos, coloracts)
    
    #Debug
    print "Debug:"
    print "hora primer dato: %s \nhora comienzo primer episodio: %s" % (datetime.datetime.fromtimestamp(tiempos[0]),  datetime.datetime.fromtimestamp(horas[0]))
    
    def episodioSiguiente(cls):
        if (cls.epAct < len(cls.indices) - 1): #Último episodio
            cls.epAct += 1
            print "Episodio: %i" % cls.epAct
            cls.barraSuenio, cls.horas, cls.consumoData, cls.flujoData, cls.tempData = creaEpisodio(cls.epAct, cls.indices, cls.colorsuenos, cls.coloracts)
            #Establecer el rango nuevo

    def episodioAnterior(cls):
        if (cls.epAct > 0): #Primer episodio
            cls.epAct -= 1
            print "Episodio: %i" % cls.epAct
            cls.barraSuenio, cls.horas, cls.consumoData, cls.flujoData, cls.tempData = creaEpisodio(cls.epAct, cls.indices, cls.colorsuenos, cls.coloracts)
        
    
        

		
