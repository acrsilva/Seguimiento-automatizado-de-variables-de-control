# -*- coding: utf-8 -*-

"""
v.02
Gestiona los episodios de sueño desde un fichero de datos
Permite obtener gráficos de barras para cada episodio de sueño
y para cada episodio de consumo energético

Columnas: (1)tiempo, (17)consumo energético, (25)clasif sueño
"""


from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
import datetime
import leeFichero as lf
import colores


PRUEBAS = 0
DEBUG = 1


def mediaMovil(x, n):
    print "Alisando"
    window= np.ones(int(n))/float(n)
    return np.convolve(x, window, 'full') #full|same


rango = 6 * 60 #Horas antes y después del episodio de sueño


class SelecEpisodio(object):
    
    def __init__(self, filename=''):
        #Obtener los datos de los episodios de sueño del fichero csv
        self.fichero = lf.LectorFichero(filename, f_sedentario=False, f_ligero=False, f_moderado=False)
        self.csv = self.fichero.datos_total
        self.eps_sueno = self.fichero.selep_completo
        
        #self.ini, self.fin, self.eini, self.efin = 0, 0, 0, 0
        self.barraSuenio = []
        self.horas = []
        self.consumoData = []
        self.flujoData = []
        #self.flujoDataNA = []
        self.tempData = []
        #self.tempDataNA = []
        self.acelData = []
        #self.metsData = []
        #self.activiData = []
        
        #Obtener indices de cada episodio de todo el intervalo de sueño
        self.ep_indices, self.su_indices = self.get_eps_indices()
        self.imprimeIndicesEp()
        self.colorsuenos = self.coloreaSueno()
        self.coloracts = self.coloreaActividades()
        
        #Elegir el episodio inicial
        self.episodio = 0
        
        self.actualizar()   
        
        #Debug
    
    
    def get_eps_indices(self):
        if(DEBUG): print 'Indices originales por cada episodio de sueño'
        #ultimo = self.csv.epFiltro[-1].fin
        ultimo = self.csv.tiempo[-1]
        ep_ind, su_ind = [], []
        for i in self.eps_sueno.epFiltro:
            if(DEBUG): print i.ini, i.fin
            if(i.ini >= rango):
                ini = i.ini-rango
            else:
                ini = 0
            if(i.fin + rango > ultimo):
                fin = ultimo
            else:
                fin = i.fin + rango
            ep_ind.append((ini, fin))
            su_ind.append((i.ini, i.fin))
        return ep_ind, su_ind
        
    def imprimeIndicesEp(self):
        print "Imprimiendo indices de episodios de sueño"

        for i in range(len(self.ep_indices)):
            print "indice %i : %i , %i - %i, %i" % (i, self.ep_indices[i][0], 
                self.su_indices[i][0], self.ep_indices[i][1], self.su_indices[i][1])
    
    def coloreaSueno(self):
        print "Coloreando sueños"
        colors = []
        num = 0
        for i in self.csv.sueno:
            if(i == 2): #Sueño ligero
                c = colores.suenoLigero
            elif(i == 4): #Sueño profundo
                c = colores.suenoProfundo
            elif(i == 5): #Sueño muy profundo
                c = colores.suenoMuyProfundo
            else: #Despierto
                c = colores.despierto
            colors.append(c)
            num = num + 1
        return colors
    
    def coloreaActividades(self):
        print "Coloreando clasificación de actividad física"
        colors = []
        num = 0
        for i in range(len(self.csv.tiempo)):
            if(self.csv.actsd[i]):
                c = colores.sedentario
            elif(self.csv.actli[i]):
                c = colores.ligero
            elif(self.csv.actmd[i]):
                c = colores.moderado
            else: #SOBRA
                print "Error de actividad"
                c = 'b' 
            colors.append(c)
            num = num + 1
        return colors
    
    
    def actualizar(self):
        #self.ini, self.fin, self.eini, self.efin = rangoEpisodio(cls.episodio, cls.indices, cls.colorsuenos, cls.coloracts)
        eini, efin, sini, sfin = self.ep_indices[self.episodio][0], self.ep_indices[self.episodio][1], self.su_indices[self.episodio][0], self.su_indices[self.episodio][1]
        self.barraSuenio = self.creaBarra(eini, efin, sini, sfin+1, self.colorsuenos, self.coloracts)
        self.horas = self.csv.tiempo[eini : efin+1]
        self.consumoData = self.csv.consm[eini:efin+1]
        #self.flujoData = flujosAlisado[eini:efin+1]
        self.flujoData = self.csv.flujo[eini:efin+1]
        #cls.tempData = temperaturasAlisado[cls.ini:cls.fin]
        self.tempData = self.csv.temp[eini:efin+1]
        self.acelData = self.csv.acltrans[eini:efin+1]
        #cls.metsData = mets[cls.ini:cls.fin]
        #cls.activiData = actividades[cls.ini:cls.fin]
    
    
    """
    Crea una barra de colores con la clasificación del sueño de un episodio de sueño
    y la clasificación de actividades durante varias horas antes y después del episodio
    """
    def creaBarra(self, ini, fin, eini, efin, cs, ca):
        print "Creando barra de colores"
        #Longitud del episodio completo
        n = fin - ini
        colors = []
        colors.extend(ca[ini:eini])
        colors.extend(cs[eini:efin])
        colors.extend(ca[efin:fin])
        
        #print len(colors)
        #print len(tiempos[ini:fin])
        
        return pg.BarGraphItem(x0=(self.csv.tiempo[ini : fin+1][ini:fin]), width=60, height=1, brushes=colors, pens=colors)

        
    
    def episodioSiguiente(self):
        if (self.episodio < len(self.ep_indices) - 1): #Último episodio
            self.episodio += 1
            print "Episodio: %i" % self.episodio
            self.actualizar()

    def episodioAnterior(self):
        if (self.episodio > 0): #Primer episodio
            self.episodio -= 1
            print "Episodio: %i" % self.episodio
            self.actualizar()
    
    
#PRUEBAS
if(PRUEBAS):
    selep = SelecEpisodio('../data.csv')
        
