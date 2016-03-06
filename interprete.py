# -*- coding: utf-8 -*-

"""
v.02
Prueba para insertar la prueba de gráfico de barras con episodio de sueño
utilizando Qt designer y generando el código dinámicamente, es decir, sin 
compilar previamente

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
import selecepisodio
import time
import datetime

pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'interfaz.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

#Etiquetas de tiempo del eje X
class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        rng = max(values)-min(values)
        if rng < 3600:
            string = '%H:%M'
        elif rng < 3600 * 24:
            string = '%d-%m-%y %H:%M'
        else:
            string = '%Y'
        for x in values:
            try:
                strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:
                strns.append('')
        return strns


def pintarDatos(p1, p2, selep):
    p1.clear()
    p1.addItem(selep.barraSuenio)
    p2.clear()
    p2.plot(x=selep.horas, y=selep.consumoData, pen=(255,0,0), name="Curva consumo")
    p2.plot(x=selep.horas, y=selep.flujoData, pen=(0, 255, 0))
    p2.plot(x=selep.horas, y=selep.tempData, pen=(255, 255, 255))
    
    #Configurar rangos iniciales de visualización
    p1.autoRange() #chapuza temporal
    p2.autoRange()
    #self.p1.setXRange(0, 100)

class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        
        #Obtener los datos del episodio a mostrar
        self.selep = selecepisodio.SelecEpisodio()
        
        #Obtener el widget de gráficos (GraphicsLayoutWidget)
        win = self.ui.plotConsumo
        
        #Configurar barra de colores con clasificación de actividad física y sueño
        self.p1 = win.addPlot(name='barClasificacion')
        self.p1.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.p1.setMouseEnabled(x=True, y=False)
        self.p1.hideAxis('left')
        self.p1.hideAxis('bottom')
        
        #Configurar gráfica inferior (consumo energético, temperaturas, etc)
        win.nextRow()
        axis = DateAxis(orientation='bottom')
        self.p2 = win.addPlot(axisItems={'bottom': axis})
        self.p2.setXLink('barClasificacion')
        self.p2.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.p2.setMouseEnabled(x=True, y=False)
        self.p2.showGrid(x=True)
        
        pintarDatos(self.p1, self.p2, self.selep)
        
        #Configurar altura de la barra
        win.ci.layout.setRowMaximumHeight(0, 80)
        
        #Configurar los botones
        self.ui.next_e_btn.clicked.connect(self.nextEp)
        self.ui.prev_e_btn.clicked.connect(self.prevEp)
        
        
        #self.p1.setLabel('top', 'Clasificación de actividad y sueño', units='')
        #self.p2.setLabel('bottom', 'Hora', units='Minutos')
        
        self.show()
        
    def nextEp(self):
        #Actualizar y mostrar el nuevo episodio
        self.selep.episodioSiguiente()
        pintarDatos(self.p1, self.p2, self.selep)
        
    def prevEp(self):
        self.selep.episodioAnterior()
        pintarDatos(self.p1, self.p2, self.selep)
 

#Inicializar interfaz
mwin = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
