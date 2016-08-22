# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from selEpisodioSueno import SelEpisodioSueno, EpisodioSueno
import colores


DEBUG = 0

"""
pg.mkQApp()
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'int_interprete.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)
"""

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
#gvInterprete = plotConsumo
class PanelInterprete():
    def __init__(self, suenos, csv, gvInterprete, btn_prev, btn_next, cbxEpisodio):
        #self.selep = selep
        self.gvInterprete = gvInterprete
        self.btn_prev = btn_prev
        self.btn_next = btn_next
        self.cbxEpisodio = cbxEpisodio
        
        self.loadData(suenos, csv)
        
        self.initGraphs()
        
        self.btn_next.clicked.connect(self.btnNextListener)
        self.btn_prev.clicked.connect(self.btnPrevListener)
        self.cbxEpisodio.activated[str].connect(self.cbxListener)
           
        
    
    def initGraphs(self):
        #Obtener el layout de gr�ficos (GraphicsLayoutWidget)
        win = self.gvInterprete
        
        #Configurar barra de colores con clasificaci�n de actividad f�sica y sue�o
        self.pBarra = win.addPlot(row=0, col=0, name='barClasificacion')
        self.pBarra.setTitle('Clasificación de actividad y sueño')
        self.pBarra.hideButtons()
        self.pBarra.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pBarra.setMouseEnabled(x=True, y=False)
        self.pBarra.hideAxis('bottom')
        self.pBarra.getAxis('left').setLabel('', color='#0000FF')
        self.pBarra.showAxis('right')
        self.pBarra.getAxis('right').setLabel('', color='#0000FF')
        
        #Configurar primera gr�fica con aceler�metros
        #win.nextRow()
        self.pAcel = win.addPlot(row=1, col=0, connect="finite")
        self.pAcel.setTitle('Acelerómetro transversal')
        self.pAcel.hideButtons()
        self.pAcel.setMouseEnabled(x=True, y=False)
        self.pAcel.hideAxis('bottom')
        self.pAcel.getAxis('left').setLabel('', color='#0000FF')
        self.pAcel.showAxis('right')
        self.pAcel.getAxis('right').setLabel('', color='#0000FF')
        self.pAcel.setXLink('barClasificacion')
        
        #Configurar segunda gr�fica con actividad f�sica y consumo
        #win.nextRow()
        self.pAF = win.addPlot(row=2, col=0, connect="finite")
        self.pAF.setTitle('Consumo energético')
        self.pAF.hideButtons()
        self.pAF.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pAF.setMouseEnabled(x=True, y=False)
        self.pAF.hideAxis('bottom')
        self.pAF.getAxis('left').setLabel('', color=colores.actividad)
        self.pAF.setXLink('barClasificacion')
        
        self.pCons = pg.ViewBox()
        self.pAF.showAxis('right')
        self.pAF.scene().addItem(self.pCons)
        self.pAF.getAxis('right').linkToView(self.pCons)
        self.pCons.setXLink(self.pAF)
        self.pAF.getAxis('right').setLabel('', color=colores.consumo)
        self.pAF.vb.sigResized.connect(self.updateViews)
        
        
        #Configurar tercera gr�fica con temperatura y flujo t�rmico
        #win.nextRow()
        axis = DateAxis(orientation='bottom')
        self.pTemp = win.addPlot(row=3, col=0, axisItems={'bottom': axis}, connect="finite")
        self.pTemp.setXLink('barClasificacion')
        self.pTemp.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pTemp.setMouseEnabled(x=True, y=False)
        self.pTemp.showGrid(x=True)
        self.pTemp.getAxis('left').setLabel('Temperatura (ºC)', color=colores.temperatura)
        #self.pTemp.hideButtons()
        
        self.pFlujo = pg.ViewBox()
        self.pTemp.showAxis('right')
        self.pTemp.scene().addItem(self.pFlujo)
        self.pTemp.getAxis('right').linkToView(self.pFlujo)
        self.pFlujo.setXLink(self.pTemp)
        #self.pFlujo.disableAutoRange(axis=pg.ViewBox.XAxis)
        self.pTemp.getAxis('right').setLabel('Flujo térmico', color=colores.flujo)
        self.pTemp.vb.sigResized.connect(self.updateViews)
        
        #Enchufar los datos
        self.pintarDatos()
        
        #Configurar tama�os del layout
        win.ci.layout.setRowMaximumHeight(0, 60)
        win.ci.layout.setRowMaximumHeight(1, 80)
        win.ci.layout.setRowMaximumHeight(2, 80)
        
        
        
    
    def openFile(self):
        self.loadData()
        self.pintarDatos()
    
    def loadData(self, suenos, csv):
        #if(DEBUG): fname = '../data.csv'
        #else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        #print "Abriendo fichero ", fname
        #self.setWindowTitle('Int�rprete de sue�os (' + fname +')')
        self.selep = SelEpisodioSueno(suenos, csv)
        self.epActual = 0
        self.configureComboBox()
    
    def configureComboBox(self):
        print "Configurando combobox"
        self.cbxEpisodio.clear()
        for i in self.selep.eps_sueno:
            self.cbxEpisodio.addItem(i.nombre)
    
    def clearGraphs(self):
        self.pBarra.clear()
        self.pAF.clear()
        self.pAcel.clear()
        self.pCons.clear()
        self.pTemp.clear()
        self.pFlujo.clear()
        
    def pintarDatos(self):
        ep = self.selep.eps_sueno[self.epActual]
        
        self.pBarra.clear()
        #self.pBarra.addItem(self.selep.barraSuenio)
        
        if(DEBUG): print len(ep.horas), len(ep.colors)
        self.pBarra.addItem(pg.BarGraphItem(x0=(ep.horas), width=60, height=1, brushes=ep.colors, pens=ep.colors))
        
        self.pAF.clear()
        #self.pAF.plot(x=self.selep.horas, y=self.selep.activiData, pen=colores.actividad)
        
        self.pAcel.clear()
        self.pAcel.plot(x=ep.horas, y=ep.acelData, pen=colores.acelerometro)
        
        self.pCons.clear()
        self.pCons.addItem(pg.PlotCurveItem(x=ep.horas, y=ep.consumoData, pen=colores.consumo))
        
        self.pTemp.clear()
        self.pTemp.plot(x=ep.horas, y=ep.tempData, pen=colores.temperatura)
        
        self.pFlujo.clear()
        self.pFlujo.addItem(pg.PlotCurveItem(x=ep.horas, y=ep.flujoData, pen=colores.flujo))
        
        #Configurar rangos iniciales de visualizaci�n
        self.pBarra.autoRange()
        self.pAF.setYRange(0,2)
        self.pCons.setYRange(0,self.selep.limConsumo)
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
        
    def btnNextListener(self):
        if(self.epActual < len(self.selep.eps_sueno)-1):
            self.epActual += 1
            self.pintarDatos()
            self.cbxEpisodio.setCurrentIndex(self.epActual)
        
    def btnPrevListener(self):
        if(self.epActual > 0):
            self.epActual -= 1
            self.pintarDatos()
            self.cbxEpisodio.setCurrentIndex(self.epActual)
    
    def cbxListener(self):
        print 'Mostrando episodio', self.cbxEpisodio.currentText()
        self.epActual = self.cbxEpisodio.currentIndex()
        self.pintarDatos()

"""
#Inicializar interfaz
mwin = MainWindow()
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
"""
