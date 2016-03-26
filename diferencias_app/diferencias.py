# -*- coding: utf-8 -*-

from PyQt4.uic import loadUiType
from PyQt4 import QtGui
import pyqtgraph as pg
import sys
import numpy as np
import sklearn as sk
from sklearn import preprocessing

csv = np.genfromtxt ('../data.csv', delimiter=",")
t = csv[:,0] / 1000 #Tiempo
a = csv[:,8] #Temperatura
b = csv[:,26] #Flujo

an = preprocessing.scale(a)
bn = preprocessing.scale(b)

app = QtGui.QApplication(sys.argv)
graph = pg.plot(t,an)
graph.plot(t,bn) 
graph.setTitle("Título")

 

app.exec_()
