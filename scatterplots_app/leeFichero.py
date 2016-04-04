# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import codecs

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
        self.sueno = self.csv['Sueño'.encode('utf-8')]
        self.flujo = self.csv['Flujo_térmico__media'.encode('utf-8')]
        self.temp = self.csv['Temp_cerca_del_cuerpo__media']
        self.tiempo = self.csv['Time']
        self.actli = self.csv['Ligera']
        self.actsd = self.csv['Sedentaria']
        self.actmd = self.csv['Moderada']
        self.consm = self.csv['Gasto_energético'.encode('utf-8')]
        self.acltrans = self.csv['Acel_transversal__picos']
"""
lee = LeeFichero('../data.csv')
print lee.nombreFichero
print lee.nparams
it = 0
print lee.nomCols
for i in lee.nomCols:
    print it, i
    it += 1
print lee.nomCols[19]
print lee.actli
print lee.nomCols[15]
print lee.sueno
print lee.nomCols[17]
print lee.consm
"""
