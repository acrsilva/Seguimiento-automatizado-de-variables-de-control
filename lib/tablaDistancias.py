# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../lib')

from pyqtgraph.Qt import QtGui
from PyQt4.QtGui import *
import colores



class TablaDistancias(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.rellenar()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    #Rellena la diagonal inferior de la tabla y colorea la distancia menor de cada fila
    def rellenar(self):
        i = self.data.shape[0]-2
        while(i >= 0):
            j=i
            if(j==0): min = j
            else: min = j-1
            while(j >= 0):
                if(self.data[i+1][j] < self.data[i+1][min]): min = j
                self.setItem(i, j, QTableWidgetItem(format(self.data[i+1][j], '.1f')))
                j -= 1
            self.item(i,min).setBackground(QtGui.QColor(colores.marcatabla))
            i -= 1
