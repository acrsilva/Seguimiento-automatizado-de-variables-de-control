# -*- coding: utf-8 -*-

"""
v.03

pyqtgraph sin bugs:
git clone https://github.com/pyqtgraph/pyqtgraph
cd pyqtgraph
sudo python setup.py install

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


class MainWindow(TemplateBaseClass):
    def pintarDatos(self):
        self.p1.clear()
        self.p1.addItem(self.selep.barraSuenio)
        
        self.p12.clear()
        self.p12.plot(x=self.selep.horas, y=self.selep.acelData, pen=(255,0,0))
        
        self.p2.clear()
        self.p2.plot(x=self.selep.horas, y=self.selep.tempData, pen=(255, 255, 255))
        self.p2.plot(x=self.selep.horas, y=self.selep.consumoData, pen=(0,0,255))
        
        self.p3.clear()
        self.p3.addItem(pg.PlotCurveItem(x=self.selep.horas, y=self.selep.flujoData, pen=(0, 255, 0)))
        
        
        #Configurar rangos iniciales de visualización
        self.p1.autoRange() #chapuza temporal
        self.p2.autoRange()
        #self.p1.setXRange(0, 100)
        #p1.setRange()
    
    def updateViews(self):
        ## view has resized; update auxiliary views to match
        self.p3.setGeometry(self.p2.vb.sceneBoundingRect())
        
        ## need to re-update linked axes since this was called
        ## incorrectly while views had different shapes.
        ## (probably this should be handled in ViewBox.resizeEvent)
        self.p3.linkedViewChanged(self.p2.vb, self.p3.XAxis)
        
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
        self.p1.setTitle('Clasificación de actividad y sueño')
        self.p1.hideButtons()
        self.p1.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.p1.setMouseEnabled(x=True, y=False)
        self.p1.hideAxis('left')
        self.p1.hideAxis('bottom')
        
        win.nextRow()
        self.p12 = win.addPlot()
        self.p12.hideButtons()
        self.p12.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.p12.setMouseEnabled(x=True, y=False)
        self.p12.hideAxis('left')
        self.p12.hideAxis('bottom')
        self.p12.setXLink('barClasificacion')
        
        
        #Configurar gráfica inferior (consumo energético, temperaturas, etc)
        win.nextRow()
        axis = DateAxis(orientation='bottom')
        self.p2 = win.addPlot(axisItems={'bottom': axis})
        self.p2.setXLink('barClasificacion')
        self.p2.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.p2.setMouseEnabled(x=True, y=False)
        self.p2.showGrid(x=True)
        self.p2.getAxis('left').setLabel('Temperatura (ºC)', color='#FFFFFF')
        self.p2.setYRange(20, 45)
        
        self.p3 = pg.ViewBox()
        self.p2.showAxis('right')
        self.p2.scene().addItem(self.p3)
        self.p2.getAxis('right').linkToView(self.p3)
        self.p3.setXLink(self.p2)
        self.p2.getAxis('right').setLabel('Flujo térmico', color='#00FF00')
        self.p2.vb.sigResized.connect(self.updateViews)

        self.pintarDatos()
        
        #Configurar altura de la barra
        win.ci.layout.setRowMaximumHeight(0, 80)
        win.ci.layout.setRowMaximumHeight(1, 50)
        
        #Configurar los botones
        self.ui.next_e_btn.clicked.connect(self.nextEp)
        self.ui.prev_e_btn.clicked.connect(self.prevEp)
        
        self.show()
    
    def nextEp(self):
        #Actualizar y mostrar el nuevo episodio
        self.selep.episodioSiguiente()
        self.pintarDatos()
        
    def prevEp(self):
        self.selep.episodioAnterior()
        self.pintarDatos()


#Inicializar interfaz
mwin = MainWindow()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
