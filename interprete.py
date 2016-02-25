# -*- coding: utf-8 -*-

"""

Prueba para insertar la prueba de gráfico de barras con episodio de sueño
utilizando Qt designer y generando el código dinámicamente, es decir, sin 
compilar previamente

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
import selecepisodio

pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'interfaz.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class MainWindow(TemplateBaseClass):  
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        #self.ui.plotBtn.clicked.connect(self.plot)
        
        #Configurar la gráfica de barras de episodios de sueño
        plt = pg.PlotItem()
        plt.getViewBox().setMouseEnabled(False, False)
        self.ui.plotBarSueno.setCentralItem(plt)
        plt.addItem(barGraphItem)
        """
        #Configurar la gráfica de consumo energético
        self.ui.plotConsumo.setLabel('left', 'Tipo de sueño', units='');
        self.ui.plotConsumo.setLabel('bottom', 'Instante', units='minutos');
        self.ui.plotConsumo.setLabel('left', 'Tipo de sueño', units='');
        self.ui.plotConsumo.setLabel('bottom', 'Instante', units='minutos');
        """
        self.show()
        
    def plot(self):
        self.ui.plot.plot(np.random.normal(size=100), clear=True)
        

selep = selecepisodio.SelecEpisodio()
barGraphItem = selep.barGraphItem

x = selep.getX()

#Inicializar interfaz
win = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
