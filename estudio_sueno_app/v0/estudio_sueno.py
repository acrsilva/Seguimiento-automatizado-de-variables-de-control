# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import matplotlib.dates as md
import math
import cachitos
import colores
import clustering

DEBUG = 1


Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')

# plotLayout
# cbx1, cbx2
# btnAbrir, btnClustering
# rbTemperatura, rbConsumo
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.__initGraphs__()
        self.loadData()
        
        #Flags
        self.showClustering = True
        self.temp = True
        self.cons = False        
        
        #Conectar elementos de la interfaz
        self.cbx1.activated[str].connect(self.cbx1Listener)
        self.cbx2.activated[str].connect(self.cbx2Listener)
        self.btnAbrir.clicked.connect(self.loadData)
        self.btnClustering.clicked.connect(self.btnClusteringListener)
        self.rbTemperatura.clicked.connect(self.rbListener)
        self.rbConsumo.clicked.connect(self.rbListener)

    #Mejorar con hide/show
    def cluster(self):
        if(self.showClustering):
            print "Mostrar dendograma y distancias"
            for cnt in reversed(range(self.vblClustering.count())):
                widget = self.vblClustering.takeAt(cnt).widget()
                if widget is not None: 
                    widget.deleteLater()
            clusters = clustering.HierarchicalClustering(self.selep, tf=self.rbTemperatura.isChecked(), cons=self.rbConsumo.isChecked())
            self.canvasCluster = FigureCanvas(clusters.getDendogram())
            self.vblClustering = QtGui.QVBoxLayout()
            self.vblClustering.addWidget(self.canvasCluster)
            self.vblClustering.addWidget(self.createTable(clusters.distancias))
            self.clusteringLayout.addLayout(self.vblClustering)
        else:
            print "Borrar dendograma"
            for cnt in reversed(range(self.vblClustering.count())):
                widget = self.vblClustering.takeAt(cnt).widget()
                if widget is not None: 
                    widget.deleteLater()

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
        
        
        self.vblClustering = QtGui.QVBoxLayout()
        #self.clusteringLayout.addLayout(self.vblClustering)
        
    def plotGraph(self, fig, tiempo, data, clear=False, temperatura=False, flujo=False, consumo=False):
        ax = fig.axes[0]
        ax.clear()
        
        if(not clear):
            ax.plot(tiempo, data, 'b-')
            if(temperatura):
                ax.set_ylabel('Temperatura (ºC)', color='b')
                ax.set_ylim([25,40])
            elif(flujo):
                ax.set_ylabel('Flujo térmico', color='b')
                ax.set_ylim([-20,220])
            elif(consumo):
                ax.set_ylabel('Consumo (cal)', color='b')
                #ax.set_ylim([-20,220])
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
            self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, temperatura=True)
            self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, flujo=True)
            self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, temperatura=True)
            self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, flujo=True)
            
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
            if(self.rbTemperatura.isChecked()):
                self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, temperatura=True)
                self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, flujo=True)
            elif(self.rbConsumo.isChecked()):
                self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, consumo=True)
                self.plotGraph(self.fig1_var2, 0, 0, clear=True)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = self.cbx2.currentIndex()
            if(self.rbTemperatura.isChecked()):
                self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, temperatura=True)
                self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, flujo=True)
            elif(self.rbConsumo.isChecked()):
                self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, consumo=True)
                self.plotGraph(self.fig2_var2, 0, 0, clear=True)
        
    class MyTable(QTableWidget):
        def __init__(self, data, *args):
            QTableWidget.__init__(self, *args)
            self.data = data
            self.setmydata()
            self.resizeColumnsToContents()
            self.resizeRowsToContents()
     
        def setmydata(self):
            for i in range(self.data.shape[0]):
                for k in range(self.data.shape[1]):
                    newitem = QTableWidgetItem(str(self.data[i][k])[:6])
                    self.setItem(i, k, newitem)
        
        
    def cbx1Listener(self, text):
        print "Episodio izquierdo", text   
        self.updateGraphs(ep2=False)
        
    def cbx2Listener(self, text):
        print "Episodio derecho", text
        self.updateGraphs(ep1=False)
    
    def rbListener(self):
        print "Radio button"
        self.updateGraphs(ep1=True, ep2=True)
        self.cluster()
        
    def createTable(self, clusters):
        horHeaders = []
        for i in self.selep.epFiltro:
            horHeaders.append(i.nombre)
        table = self.MyTable(clusters, len(clusters), len(clusters))
        table.setHorizontalHeaderLabels(horHeaders)
        table.setVerticalHeaderLabels(horHeaders)
        return table
                
    def btnClusteringListener(self):
        if(not self.showClustering):
            print "Mostrar dendograma y distancias"
            self.showClustering = True
            self.cluster()
        else:
            self.showClustering = False
            self.cluster()
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    sys.exit(app.exec_())
    
    
