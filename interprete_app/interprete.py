# -*- coding: utf-8 -*-

"""
v.03

pyqtgraph sin bugs:
git clone https://github.com/pyqtgraph/pyqtgraph
cd pyqtgraph
sudo python setup.py install

"""
from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
import selecepisodio
import time
#import datetime

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
        self.pBarra.clear()
        self.pBarra.addItem(self.selep.barraSuenio)
        
        self.pAF.clear()
        self.pAF.plot(x=self.selep.horas, y=self.selep.activiData, pen=(255, 126, 0))
        
        self.pAcel.clear()
        self.pAcel.plot(x=self.selep.horas, y=self.selep.acelData, pen=(255,0,0))
        
        self.pCons.clear()
        self.pCons.addItem(pg.PlotCurveItem(x=self.selep.horas, y=self.selep.consumoData, pen=(0,224,0)))
        
        self.pTemp.clear()
        self.pTemp.plot(x=self.selep.horas, y=self.selep.tempData, pen=(255, 255, 255))
        
        self.pFlujo.clear()
        self.pFlujo.addItem(pg.PlotCurveItem(x=self.selep.horas, y=self.selep.flujoData, pen=(0, 255, 0)))
        
        #Configurar rangos iniciales de visualización
        self.pBarra.autoRange()
        self.pAF.setYRange(0,2)
        self.pCons.setYRange(0,65)
        self.pTemp.setYRange(20,45)
        self.pFlujo.setYRange(-20, 220)
    
    def updateViews(self):
        ## view has resized; update auxiliary views to match
        self.pFlujo.setGeometry(self.pTemp.vb.sceneBoundingRect())
        
        ## need to re-update linked axes since this was called
        ## incorrectly while views had different shapes.
        ## (probably this should be handled in ViewBox.resizeEvent)
        self.pFlujo.linkedViewChanged(self.pTemp.vb, self.pFlujo.XAxis)
        
        self.pCons.setGeometry(self.pAF.vb.sceneBoundingRect())
        self.pCons.linkedViewChanged(self.pAF.vb, self.pCons.XAxis)
        
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        
        #Obtener los datos del episodio a mostrar
        self.selep = self.loadData()
        
        #Obtener el layout de gráficos (GraphicsLayoutWidget)
        win = self.ui.plotConsumo
        
        #Configurar barra de colores con clasificación de actividad física y sueño
        self.pBarra = win.addPlot(name='barClasificacion')
        self.pBarra.setTitle('Clasificación de actividad y sueño')
        self.pBarra.hideButtons()
        self.pBarra.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pBarra.setMouseEnabled(x=True, y=False)
        self.pBarra.hideAxis('bottom')
        self.pBarra.getAxis('left').setLabel('', color='#0000FF')
        self.pBarra.showAxis('right')
        self.pBarra.getAxis('right').setLabel('', color='#0000FF')
        
        #Configurar primera gráfica con acelerómetros
        win.nextRow()
        self.pAcel = win.addPlot()
        self.pAcel.setTitle('Acelerómetros')
        self.pAcel.hideButtons()
        self.pAcel.setMouseEnabled(x=True, y=False)
        self.pAcel.hideAxis('bottom')
        self.pAcel.getAxis('left').setLabel('', color='#0000FF')
        self.pAcel.showAxis('right')
        self.pAcel.getAxis('right').setLabel('', color='#0000FF')
        self.pAcel.setXLink('barClasificacion')
        
        #Configurar segunda gráfica con actividad física y consumo
        win.nextRow()
        self.pAF = win.addPlot()
        self.pAF.setTitle('Actividad física y consumo energético')
        self.pAF.hideButtons()
        self.pAF.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pAF.setMouseEnabled(x=True, y=False)
        self.pAF.hideAxis('bottom')
        self.pAF.getAxis('left').setLabel('Actividad', color='#FF7E00')
        self.pAF.setXLink('barClasificacion')
        
        self.pCons = pg.ViewBox()
        self.pAF.showAxis('right')
        self.pAF.scene().addItem(self.pCons)
        self.pAF.getAxis('right').linkToView(self.pCons)
        self.pCons.setXLink(self.pAF)
        self.pAF.getAxis('right').setLabel('Consumo', color='#00E000')
        self.pAF.vb.sigResized.connect(self.updateViews)
        
        
        #Configurar tercera gráfica con temperatura y flujo térmico
        win.nextRow()
        axis = DateAxis(orientation='bottom')
        self.pTemp = win.addPlot(axisItems={'bottom': axis})
        self.pTemp.setXLink('barClasificacion')
        self.pTemp.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pTemp.setMouseEnabled(x=True, y=False)
        self.pTemp.showGrid(x=True)
        self.pTemp.getAxis('left').setLabel('Temperatura (ºC)', color='#FFFFFF')
        #self.pTemp.hideButtons()
        
        self.pFlujo = pg.ViewBox()
        self.pTemp.showAxis('right')
        self.pTemp.scene().addItem(self.pFlujo)
        self.pTemp.getAxis('right').linkToView(self.pFlujo)
        self.pFlujo.setXLink(self.pTemp)
        #self.pFlujo.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pTemp.getAxis('right').setLabel('Flujo térmico', color='#00FF00')
        self.pTemp.vb.sigResized.connect(self.updateViews)
        
        #Enchufar los datos
        self.pintarDatos()
        
        #Configurar tamaños del layout
        win.ci.layout.setRowMaximumHeight(0, 60)
        win.ci.layout.setRowMaximumHeight(1, 80)
        win.ci.layout.setRowMaximumHeight(2, 80)
        
        #Configurar los botones
        self.ui.next_e_btn.clicked.connect(self.nextEp)
        self.ui.prev_e_btn.clicked.connect(self.prevEp)
        self.ui.btnLoadFile.clicked.connect(self.openFile)
        
        self.show()
        
    def openFile(self):
        self.selep = self.loadData()
        self.pintarDatos()
    
    def loadData(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        #selep = cachitos.selEpisodio(fname)
        selep = selecepisodio.SelecEpisodio(fname)
        return selep
        
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
