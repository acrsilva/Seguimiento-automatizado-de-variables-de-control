# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import episodios    

csv = np.genfromtxt ('../data.csv', delimiter=",")
t = csv[:,0] / 1000 #Tiempo
a = csv[:,8] #Temperatura
b = csv[:,26] #Flujo
#X = np.c_[a,b]



class Episodios():
    def __init__(self):
        self.numEpisodios = 3
        self.epActual = 0
        
        self.tiempo1 = t[0:255]
        self.temp1 = a[0:255]
        self.flujo1 = b[0:255]
        
        self.tiempo2 = t[0:255]
        self.temp2 = a[0:255]
        self.flujo2 = b[0:255]
        
        self.tiempo3 = []
        self.temp3 = []
        self.flujo3 = []
        
        self.lbl1 = "sueño"
        self.lbl2 = "sedentario"
        self.lbl3 = "ligera"
    
    def epSiguiente(self):
        print "episodio siguiente"
        
    def epAnterior(self):
        print "episodio anterior"
