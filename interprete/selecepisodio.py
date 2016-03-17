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
    a = False #Episodio empezado
    c = 0 #Indice de comienzo
    t = 0 #Contador de minutos despierto
    f = 0 #
    for i in range(len(suenos)):
        if(not a and suenos[i] != 0): #nuevo episodio
            c = i
            a = True
            f = i
        elif(a): #episodio comenzado
            if(suenos[i] != 0): #dormido(resetear tiempo despierto)
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
        if(i == 0): #ligera
            c = pg.mkColor(255, 51, 51)
        if(i == 1): #moderada
            c = pg.mkColor(102, 255, 102)
        elif(i == 2): #alta
            c = pg.mkColor(0, 102, 0)
        else: #sin actividad
            c = pg.mkColor(85, 120, 85)  
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

def mediaMovil(x, n):
    print "Alisando"
    window= np.ones(int(n))/float(n)
    return np.convolve(x, window, 'full') #full|same

def rangoEpisodio(ep, ind, colorsuenos, coloracts):
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
    
    return ini, fin, eini, efin


#Cargar datos
csv = np.genfromtxt ('data.csv', delimiter=",")
tiempos = csv[:,0] / 1000 #Tiempo en minutos
suenos = csv[:,25] #Clasificador de sueño
consumos = csv[:,17] #Consumo energético
temperaturas = csv[:,8] #Temperatura media (piel-4, 8-cuerpo)
flujos = csv[:,26] #Flujo térmico
aceleraciones = csv[:,1] #Acel. transversal
actividades = cargarActividad()
flujosAlisado = mediaMovil(flujos, 5)
temperaturasAlisado = mediaMovil(temperaturas, 5)
mets = csv[:,21]

rango = 6 * 60 #Horas antes y después del episodio de sueño


class SelecEpisodio(object):
    def actualizar(cls):
        cls.ini, cls.fin, cls.eini, cls.efin = rangoEpisodio(cls.episodio, cls.indices, cls.colorsuenos, cls.coloracts)
        cls.barraSuenio = creaBarra(cls.ini, cls.fin, cls.eini, cls.efin+1, cls.colorsuenos, cls.coloracts)
        cls.horas = tiempos[cls.ini : cls.fin]
        cls.consumoData = consumos[cls.ini:cls.fin]
        cls.flujoData = flujosAlisado[cls.ini:cls.fin]
        #cls.flujoDataNA = flujos[cls.ini:cls.fin]
        cls.tempData = temperaturasAlisado[cls.ini:cls.fin]
        #cls.tempDataNA = temperaturas[cls.ini:cls.fin]
        cls.acelData = aceleraciones[cls.ini:cls.fin]
        cls.metsData = mets[cls.ini:cls.fin]
        cls.activiData = actividades[cls.ini:cls.fin]
        
    def __init__(self):
        self.ini = 0
        self.fin = 0
        self.eini = 0
        self.efin = 0
        self.barraSuenio = []
        self.horas = []
        self.consumoData = []
        self.flujoData = []
        #self.flujoDataNA = []
        self.tempData = []
        #self.tempDataNA = []
        self.acelData = []
        self.metsData = []
        self.activiData = []
        
        #Obtener indices de cada episodio de todo el intervalo de sueño
        self.indices = trocear()
        imprimeIndicesEp(self.indices)
        self.colorsuenos = coloreaSueno()
        self.coloracts = coloreaActividades()
        
        #Elegir el episodio inicial
        self.episodio = 0
        
        self.actualizar()   
        
        #Debug
    
    def episodioSiguiente(cls):
        if (cls.episodio < len(cls.indices) - 1): #Último episodio
            cls.episodio += 1
            print "Episodio: %i" % cls.episodio
            cls.actualizar()

    def episodioAnterior(cls):
        if (cls.episodio > 0): #Primer episodio
            cls.episodio -= 1
            print "Episodio: %i" % cls.episodio
            cls.actualizar()
    
    
    

		
