# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.dates as md
import math
import cachitos
import colores
import clustering

DEBUG = 0



Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')

# plotLayout
# cbx1, cbx2
# checkTemp, checkFlujo
# btnAbrir, btnCluster
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        
        self.__initGraphs__()
        self.loadData()
        
        #Conectar elementos de la interfaz
        self.cbx1.activated[str].connect(self.cbx1Listener)
        self.cbx2.activated[str].connect(self.cbx2Listener)
        self.btnAbrir.clicked.connect(self.loadData)
        self.checkClustering.clicked.connect(self.checkClusteringListener)
        self.checkTemp.clicked.connect(self.checkTempListener)
        self.checkFlujo.clicked.connect(self.checkFlujoListener)
        
    
    def __initGraphs__(self):
        #Graficas izquierda
        self.fig1_var1 = plt.figure(tight_layout=True)
        self.fig1_var1.add_subplot(111)
        self.fig1_var2 = plt.figure(tight_layout=True)
        self.fig1_var2.add_subplot(111)
        self.canvas11 = FigureCanvas(self.fig1_var1)
        canvas12 = FigureCanvas(self.fig1_var2)
        vbox1 = QtGui.QGridLayout()
        vbox1.addWidget(self.canvas11)
        vbox1.addWidget(canvas12)
        
        #Graficas derecha
        self.fig2_var1 = plt.figure(tight_layout=True)
        self.fig2_var1.add_subplot(111)
        self.fig2_var2 = plt.figure(tight_layout=True)
        self.fig2_var2.add_subplot(111)
        canvas21 = FigureCanvas(self.fig2_var1)
        canvas22 = FigureCanvas(self.fig2_var2)
        vbox2 = QtGui.QGridLayout()
        vbox2.addWidget(canvas21)
        vbox2.addWidget(canvas22)
        
        self.plotLayout.addLayout(vbox1)
        self.plotLayout.addLayout(vbox2)
        
        self.f = plt.figure("Dendogram")
    
    def plotGraph(self, fig, tiempo, data, limMin, limMax, clear=False):
        ax = fig.axes[0]
        ax.clear()
        
        if(not clear):
            ax.plot(tiempo, data, 'b-')
        ax.set_ylabel('Temperatura (ºC)', color='b')
        ax.set_ylim([limMin,limMax])
        for tl in ax.get_yticklabels():
            tl.set_color('b')
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        start, end = ax.get_xlim()
        ax.grid(True)
        
        #fig.canvas.update()
        fig.canvas.draw()
    
    def configureComboBox(self):
        print "Configurando combobox"
        self.cbx1.clear()
        self.cbx2.clear()
        #Solución temporal, el nombre debe ser el del propio Episodio!!!!!
        for i in self.selep.epFiltro:
            self.cbx1.addItem(i.nombre)
            self.cbx2.addItem(i.nombre)
   
    def loadData(self):
        def updateUI():
            print "Actualizando interfaz"
            #idx = int(self.cbx1.currentText()[5])
            #idx = self.getCbxIdx()
            idx = self.cbx1.currentIndex()
            self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, 25, 40)
            self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, -20, 220)
            self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, 25, 40)
            self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, -20, 220)
            
        if(DEBUG): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        
        print "Abriendo fichero ", fname
        self.selep = cachitos.selEpisodio(fname, sedentario=False, ligero=False, moderado=False)
        self.configureComboBox()
        updateUI()
        
    def updateGraphs(self, ep1=True, ep2=True):
        if(ep1):
            print "Actualizar episodio izquierdo"
            idx = self.cbx1.currentIndex()
            if(self.checkTemp.isChecked()):
                self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, 25, 40)
            else:
                self.plotGraph(self.fig1_var1, 0, 0, 25, 40, clear=True)
            if(self.checkFlujo.isChecked()):
                self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, -20, 220)
            else:
                self.plotGraph(self.fig1_var2, 0, 0, 25, 40, clear=True)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = self.cbx2.currentIndex()
            if(self.checkTemp.isChecked()):
                self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, 25, 40)
            else:
                self.plotGraph(self.fig2_var1, 0, 0, 25, 40, clear=True)
            if(self.checkFlujo.isChecked()):
                self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, -20, 220)
            else:
                self.plotGraph(self.fig2_var2, 0, 0, 25, 40, clear=True)
        
    
        
    def cbx1Listener(self, text):
        print "Episodio izquierdo", text   
        self.updateGraphs(ep2=False)
        
    def cbx2Listener(self, text):
        print "Episodio derecho", text
        self.updateGraphs(ep1=False)
        
    def checkTempListener(self):
        print "Filtrar Temperatura"
        self.updateGraphs()
        
    def checkFlujoListener(self):
        print "Filtrar Flujo"
        self.updateGraphs()
            
    def checkClusteringListener(self):
        if(self.checkClustering.isChecked()):
            print "Mostrar dendograma"
            #self.clusters = clustering.HierarchicalClustering(self.selep)
            self.f = clustering.HierarchicalClustering(self.selep).getDendogram()
            self.f.show()
            """
            f = plt.figure('Clustering')
            plt.title('Dendograma de clustering jerarquico')
            plt.xlabel('Indice de episodio')
            plt.ylabel('Distancia')
            plt.plot(self.selep.epFiltro[0].tiempo, self.selep.epFiltro[0].flujo)
            f.show()
            """
        else:
            print "Cerrar dendograma"
            plt.close(self.f)
        
    

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    sys.exit(app.exec_())
    
    
