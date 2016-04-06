# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import codecs
import sys
from PyQt4 import QtGui

class LeeFichero(object):
    """
    Inicializa la matriz con los valores del csv
    
    Parametros de entrada
    - nombre: nombre del fichero csv que contiene los datos
    """
    def __init__(self, nombre):
        self.nombreFichero = nombre
        self.csv = np.genfromtxt(nombre, delimiter="," , names=True)
        self.nomCols = self.csv.dtype.names
        self.nparams = len(self.nomCols)
        self.sueno = self.csv['Sueño'.encode('iso8859-15')]
        self.clasifSueno = self.csv['Clasificaciones_del_sueño'.encode('iso8859-15')]
        self.flujo = self.csv['Flujo_térmico__media'.encode('iso8859-15')]
        self.temp = self.csv['Temp_cerca_del_cuerpo__media']
        self.tiempo = self.csv['Time'] / 1000
        self.actli = self.csv['Ligera']
        self.actsd = self.csv['Sedentaria']
        self.actmd = self.csv['Moderada']
        self.consm = self.csv['Gasto_energético'.encode('iso8859-15')]
        self.acltrans = self.csv['Acel_transversal__picos']
        
        
"""        
class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__() 
    
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        lee = LeeFichero(open(fname, 'r'))
        print lee.nomCols[19]
        print lee.actli
        print lee.nomCols[15]
        print lee.sueno
        print lee.nomCols[17]
        print lee.consm
    
    
app = QtGui.QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())        

"""
