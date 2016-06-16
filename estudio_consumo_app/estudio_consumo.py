# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
import lectorFichero as lf
import colores
import hover
import datetime 
import cachitos
from time import mktime
from datetime import datetime
from panelConsumo import PanelConsumo


DEBUG = 1
PRUEBAS = 1

Ui_MainWindow, QMainWindow = loadUiType('int_consumos.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        
        #self.initGraphs()
        self.loadData()
        
        """
        self.cbx_izq.activated[str].connect(self.cbxIzqListener)
        self.cbx_der.activated[str].connect(self.cbxDerListener)
        """
        
        self.actionAbrir.triggered.connect(self.loadData)
    
        
    def loadData(self):
        if(PRUEBAS): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        
        print "Abriendo fichero ", fname
        
        self.setWindowTitle('Estudio de sueños (' + fname +')')
        
        csv_dias = lf.LectorFichero(fname).getDatosDias()
        self.epsDias = []
        for i in csv_dias:
            self.epsDias.append(cachitos.selEpisodio(i))
        print len(self.epsDias), 'dias'
        
        self.panel = PanelConsumo(self.epsDias, self.layout_diario, self.layout_dia_izq, self.layout_dia_der,
                                  self.cbx_izq, self.cbx_der, self.lbl_izq, self.lbl_der)
        
        """
        self.ldias = []
        
        self.initCombobox()
        self.plotGraph(self.fig_izq, self.cbx_izq.currentIndex())
        self.plotGraph(self.fig_der, self.cbx_der.currentIndex())
        self.plotBarDiario()
        
        self.setLabel(izq=True)
        self.setLabel(izq=False)
        """

    
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
