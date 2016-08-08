# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
#from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import selEpisodio
import matplotlib.dates as md
from sklearn import preprocessing
import colores
import lectorFichero as lf

DEBUG = 0

    

class PanelScatter():
    def __init__(self, selep, layout, cbSueno, cbSedentario, cbLigera, cbModerada, cbIzq, cbDer, btnPrev, btnNext, label):
        self.layoutMatplot1 = layout
        self.cbSueno = cbSueno
        self.cbSedentario = cbSedentario
        self.cbLigera = cbLigera
        self.cbModerada = cbModerada
        self.cbx_izq = cbIzq
        self.cbx_der = cbDer
        self.btnPrev = btnPrev
        self.btnNext = btnNext
        self.label = label
        
        self.selep = selep
        self.configureComboBox()
        self.updateView()
        
        self.cbSueno.clicked.connect(self.filtrarSueno)
        self.cbSedentario.clicked.connect(self.filtrarSedentario)
        self.cbLigera.clicked.connect(self.filtrarLigera)
        self.cbModerada.clicked.connect(self.filtrarModerada)
        self.btnPrev.clicked.connect(self.retroceder)
        self.btnNext.clicked.connect(self.avanzar)
        self.cbx_izq.activated[str].connect(self.cbx_izqListener)
        self.cbx_der.activated[str].connect(self.cbx_derListener)
        
        
        self.filSueno = True
        self.filSedentario = True
        self.filLigero =True
        self.filModerado = True
        
    def configureComboBox(self):
        print "Configurando combobox"
        self.cbx_izq.clear()
        self.cbx_der.clear()
        for i in self.selep.epFiltro:
            self.cbx_izq.addItem(i.nombre)
            self.cbx_der.addItem(i.nombre)
        if(len(self.selep.epFiltro) > 1):
            self.cbx_der.setCurrentIndex(1)
        else: 
            self.cbx_der.setCurrentIndex(0)
        self.cbx_izq.setCurrentIndex(0)
        
        
    def openFile(self):
        self.selep = self.loadData()
        self.configureComboBox()
        self.limpiarLayout()
        self.updateView()
        
    
    def loadData(self):
        if(DEBUG): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        csv = lf.LectorFichero(fname).getDatos()
        selep = selEpisodio.selEpisodio(csv)
        return selep
    
    #ep 0 -> plot izquierdo
    #ep 1 -> plot derecho
    def getTime(self, a, b, ep):
        if(ep == 0):
            cbxId = self.cbx_izq.currentIndex()
        else:
            cbxId = self.cbx_der.currentIndex()
        print "get time", cbxId
        for i in self.selep.epFiltro[cbxId].temp:
            if(a == i):
                ind = 0
                for k in self.selep.epFiltro[cbxId].flujo:
                    if(b == k):
                        print "encontrado"
                        return self.selep.epFiltro[cbxId].tiempo[ind]
                    else:
                        ind += 1
    
    def onpick(self, event, ep):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        print xdata[ind[0]], ydata[ind[0]]
        self.label.setText('Instante ' + str(self.getTime(xdata[ind[0]], ydata[ind[0]], ep)))
            
    def creaFiguras(self, t, a, b):
        #Serie temporal
        fig0 = plt.figure(tight_layout=True)
        #Normalizar
        preprocessing.scale(a, copy=True)
        preprocessing.scale(b, copy=True)
        #Curva temperatura
        ax1 = fig0.add_subplot(111)
        ax1.plot(t, a, '-', color=colores.temperatura)
        #ax1.set_ylim([-5,5])
        #ax1.set_xlabel('Tiempo (m)')
        ax1.set_ylabel('Temperatura (ºC)', color=colores.temperatura)
        for tl in ax1.get_yticklabels():
            tl.set_color(colores.temperatura)
        fig0.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(xfmt)
        
        start, end = ax1.get_xlim()
        #ax1.xaxis.set_ticks(np.arange(start, end, 30))
        ax1.grid(True)
        
        #Curva flujo térmico
        ax2 = ax1.twinx()
        ax2.plot(t, b, '-', color=colores.flujo)
        #ax2.set_ylim([-5,5])
        ax2.set_ylabel('Flujo térmico', color=colores.flujo)
        for tl in ax2.get_yticklabels():
            tl.set_color(colores.flujo)
        
        #Scatterplot
        fig1 = plt.figure(tight_layout=True)
        ax1f1 = fig1.add_subplot(111)
        line, = ax1f1.plot(a, b, 'o', picker=5)
        #ax1f1.set_xlim([20,45])
        #ax1f1.set_ylim([-20,220])
        ax1f1.set_xlabel('Temperatura (ºC)', color=colores.temperatura)
        ax1f1.set_ylabel('Flujo térmico', color=colores.flujo)
        
        return fig0, fig1
    
    def crearWidget(self, filtro, ep):
        fig10, fig11 = self.creaFiguras(filtro.tiempo, filtro.temp, filtro.flujo)
        canvas1 = FigureCanvas(fig10)
        canvas2 = FigureCanvas(fig11)
        vbox = QtGui.QGridLayout()
        vbox.addWidget(QtGui.QLabel("<b>Episodio:</b> " + filtro.nombre))
        vbox.addWidget(QtGui.QLabel("<b>Inicio:</b> " + str(filtro.tiempo[0])))
        vbox.addWidget(QtGui.QLabel("<b>Final:</b> " + str(filtro.tiempo[-1])))
        vbox.addWidget(QtGui.QLabel("<b>Duración:</b> %i min" % (len(filtro.tiempo))))
        vbox.addWidget(QtGui.QLabel("<b>Coeficiente de correlación:</b> " + str(filtro.correlacion)[:5]))
        vbox.addWidget(QtGui.QLabel("<b>Calorías consumidas:</b> " + str(filtro.numCalorias)[:6] + " (" + str(filtro.numCalorias/self.selep.totalCal*100)[:4] + "%)"))
        vbox.addWidget(canvas1)
        vbox.addWidget(canvas2)
        canvas2.mpl_connect('pick_event', lambda event: self.onpick(event, ep))
        return vbox
    
    #Inserta elementos en el layout con los nuevos episodios
    def updateView(self):
        if(len(self.selep.epFiltro) > 0):
            self.vbox = self.crearWidget(self.selep.epFiltro[self.cbx_izq.currentIndex()], 0)
            self.layoutMatplot1.addLayout(self.vbox)
            if(len(self.selep.epFiltro) > 1):
                self.vbox2 = self.crearWidget(self.selep.epFiltro[self.cbx_der.currentIndex()], 1)
                self.layoutMatplot1.addLayout(self.vbox2)
                
    #Elimina el contenido del layout actual        
    def limpiarLayout(self):
        plt.close('all') #Cerrar todos las gráficas dibujadas para vaciar memoria   
        for cnt in reversed(range(self.vbox.count())):
            widget = self.vbox.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater() 
        for cnt in reversed(range(self.vbox2.count())):
            widget = self.vbox2.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater()
 
    def filtrarSueno(self):
        print "Filtrar sueño", self.cbSueno.isChecked()
        self.filSueno = self.cbSueno.isChecked() #Cambiar el filtro
        self.selep.update(self.filSueno, self.filSueno, self.filSedentario, self.filLigero, self.filModerado) #Actualizar el array de episodios filtrados
        self.configureComboBox()
        self.limpiarLayout()
        self.updateView()
        
        
    def filtrarSedentario(self):
        print "Filtrar sedentario"
        self.filSedentario = self.cbSedentario.isChecked()
        self.selep.update(self.filSueno, self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.configureComboBox()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarLigera(self):
        print "Filtrar ligera"
        self.filLigero = self.cbLigera.isChecked()
        self.selep.update(self.filSueno, self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.configureComboBox()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarModerada(self):
        print "Filtrar moderada"
        self.filModerado = self.cbModerada.isChecked()
        self.selep.update(self.filSueno, self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.configureComboBox()
        self.limpiarLayout()
        self.updateView()
    
    def retroceder(self):
        idxI = self.cbx_izq.currentIndex()
        idxD = self.cbx_der.currentIndex()
        if (idxI > 0):
            self.cbx_izq.setCurrentIndex(idxI-1)
        if(idxD > 0):
            self.cbx_der.setCurrentIndex(idxD-1)
        print "episodios", self.cbx_izq.currentIndex(), "y", self.cbx_der.currentIndex()
        self.limpiarLayout()
        self.updateView()
        
    def avanzar(self):
        idxI = self.cbx_izq.currentIndex()
        idxD = self.cbx_der.currentIndex()
        if (idxI < len(self.selep.epFiltro) - 1):
            self.cbx_izq.setCurrentIndex(idxI+1)
        if(idxD < len(self.selep.epFiltro) - 1):
            self.cbx_der.setCurrentIndex(idxD+1)
        print "episodios", self.cbx_izq.currentIndex(), "y", self.cbx_der.currentIndex()
        self.limpiarLayout()
        self.updateView()
        
    def cbx_izqListener(self):
        print "episodios", self.cbx_izq.currentIndex(), "y", self.cbx_der.currentIndex()
        self.limpiarLayout()
        self.updateView()
        
    def cbx_derListener(self):
        print "episodios", self.cbx_izq.currentIndex(), "y", self.cbx_der.currentIndex()
        self.limpiarLayout()
        self.updateView() 
 
    
