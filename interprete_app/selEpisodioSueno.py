# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time
import datetime
import lectorFichero as lf
import colores

from cachitos import Episodio, selEpisodio


PRUEBAS = 0
DEBUG = 1

#FALTA NORMALIZAR LOS DATOS!

class EpisodioSueno():
    def __init__(self, nombre, ep_ini, ep_fin, sueno_ini, sueno_fin, 
            colors, tiempo, consumo, flujo, temperatura, acelerometro):
        
        self.nombre = nombre
        self.ep_ini = ep_ini
        self.ep_fin = ep_fin
        self.sueno_ini = sueno_ini
        self.sueno_fin = sueno_fin
        
        self.colors = colors
        self.barraSuenio = pg.BarGraphItem(x0=tiempo, width=60, height=1, brushes=colors, pens=colors)
        self.horas = tiempo #Horas int
        self.consumoData = consumo
        self.flujoData = flujo
        #self.flujoDataNA = []
        self.tempData = temperatura
        #self.tempDataNA = []
        self.acelData = acelerometro #Acelerómetro transversal
        #self.metsData = []
        #self.activiData = []
        

class SelEpisodioSueno(object):
    def __init__(self, filename=''):
        self.csv = lf.LectorFichero(filename).getDatos()
        selep = selEpisodio(self.csv, sedentario=False, ligero=False, moderado=False).epFiltro
        
        self.eps_sueno= []
        for i in selep:
            self.eps_sueno.append(self.initEpisodio(i))
        
    #Crea un EpisodioSueno a partir de un episodio dado
    def initEpisodio(self, episodio):
        #Obtener indices de inicio y fin del episodio completo
        rango = 6 * 60 #Horas antes y después del episodio de sueño
        ultimo = len(self.csv.tiempo)-1
        if(episodio.ini >= rango):
            ep_ini = episodio.ini-rango
        else:
            ep_ini = 0
        if(episodio.fin + rango > ultimo):
            ep_fin = ultimo
        else:
            ep_fin = episodio.fin + rango
        su_ini, su_fin = episodio.ini, episodio.fin
        
        #COMPROBAR RANGOS
        #Obtener colores antes, durante y despues del episodio
        colors = []
        colors.extend(self.coloreaActividades(ep_ini, su_ini))
        colors.extend(self.coloreaSueno(su_ini, su_fin))
        colors.extend(self.coloreaActividades(su_fin, ep_fin))    
        
        return EpisodioSueno(episodio.nombre, ep_ini, ep_fin, su_ini, su_fin, 
                    colors, self.csv.tiempo[ep_ini:ep_fin+1],
                    self.csv.consm[ep_ini:ep_fin+1], self.csv.flujo[ep_ini:ep_fin+1],
                    self.csv.temp[ep_ini:ep_fin+1], self.csv.acltrans[ep_ini:ep_fin+1])
    
    #Devuelve una lista de colores según la clasificación des sueño 
    #en el intervalo especificado    
    def coloreaSueno(self, ini, fin):
        colors = []
        num = 0
        for i in self.csv.clasifSueno[ini:fin+1]:
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
    
    #Devuelve una lista de colores según la clasificación de actividad
    #en el intervalo especificado
    #COMPROBAR RANGOS Y VALORES 
    def coloreaActividades(self, ini, fin):
        colors = []
        i = ini
        while(i < fin):
            if(self.csv.actsd[i]):
                c = colores.sedentario
            elif(self.csv.actli[i]):
                c = colores.ligero
            elif(self.csv.actmd[i]):
                c = colores.moderado
            else: #SOBRA
                print "Error de actividad"
                c = 'r' 
            colors.append(c)
            i += 1
        return colors
    
    
if(PRUEBAS==1):
    SelEpisodioSueno('../data.csv')
    
