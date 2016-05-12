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
from scipy.cluster.hierarchy import dendrogram
from datetime import datetime

DEBUG = 1


Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')

class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    #Rellena la diagonal inferior de la tabla y colorea la menor distancia de cada fila
    def setmydata(self):
        i = self.data.shape[0]-1
        while(i >= 0):
            j=i
            if(j==0): min = j
            else: min = j-1
            while(j >= 0):
                if(i != j and self.data[i][j] < self.data[i][min]): min = j
                self.setItem(i, j, QTableWidgetItem(format(self.data[i][j], '.1f')))
                j -= 1
            self.item(i,min).setBackground(QtGui.QColor(colores.marcatabla))
            i -= 1

# plotLayout
# cbx1, cbx2
# btnAbrir, btnClustering
# rbTemperatura, rbConsumo
# tableDistancias
# wgDendograma
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        #self.showMaximized()
        self.setupUi(self)
        
        #Flags
        self.temp = True
        self.cons = False
        
        self.__initGraphs__()
        self.loadData()
        
        print "Listo"

        #Conectar elementos de la interfaz
        self.cbx1.activated[str].connect(self.cbx1Listener)
        self.cbx2.activated[str].connect(self.cbx2Listener)
        self.actionAbrir.triggered.connect(self.loadData)
        self.rbTemperatura.clicked.connect(self.rbListener)
        self.rbConsumo.clicked.connect(self.rbListener)

    
    #Inicializa las figuras de cada layout en las que se va a dibujar las gráficas
    def __initGraphs__(self):
        #Graficas superior
        self.fig1_var1 = plt.figure(tight_layout=True)
        self.fig1_var1.add_subplot(111)
        self.fig1_var2 = plt.figure(tight_layout=True)
        self.fig1_var2.add_subplot(111)
        self.fig1_var3 = plt.figure(tight_layout=True)
        self.fig1_var3.add_subplot(111)
        canvas11 = FigureCanvas(self.fig1_var1)
        canvas12 = FigureCanvas(self.fig1_var2)
        canvas13 = FigureCanvas(self.fig1_var3)

        self.plotLayoutUp.addWidget(canvas11)
        self.plotLayoutUp.addWidget(canvas12)
        self.plotLayoutUp.addWidget(canvas13)
        
        #Graficas inferior
        self.fig2_var1 = plt.figure(tight_layout=True)
        self.fig2_var1.add_subplot(111)
        self.fig2_var2 = plt.figure(tight_layout=True)
        self.fig2_var2.add_subplot(111)
        self.fig2_var3 = plt.figure(tight_layout=True)
        self.fig2_var3.add_subplot(111)
        canvas21 = FigureCanvas(self.fig2_var1)
        canvas22 = FigureCanvas(self.fig2_var2)
        canvas23 = FigureCanvas(self.fig2_var3)

        self.plotLayoutBot.addWidget(canvas21)
        self.plotLayoutBot.addWidget(canvas22)
        self.plotLayoutBot.addWidget(canvas23)
        
        
        
    #Carga un fichero de datos csv y lo trocea en episodios de sueño
    #Actualiza el contenido de toda la interfaz
    def loadData(self):
        if(DEBUG): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        
        print "Abriendo fichero ", fname
        self.selep = cachitos.selEpisodio(fname, sedentario=False, ligero=False, moderado=False)
        self.configureComboBox()
        self.updatePlots(ep1=True, ep2=True)
        self.initCluster()
        self.cluster()
    
    # Añade los nombres de los episodios en las listas desplegables
    def configureComboBox(self):
        print "Configurando combobox"
        self.cbx1.clear()
        self.cbx2.clear()
        for i in self.selep.epFiltro:
            self.cbx1.addItem(i.nombre)
            self.cbx2.addItem(i.nombre)
        if(len(self.selep.epFiltro) > 1):
            self.cbx2.setCurrentIndex(1)
        
        
    #Actualiza el contenido de las gráficas con el episodio seleccionado por los combobox
    def updatePlots(self, ep1=False, ep2=False):
        def getDespierto(epi):
            desp = self.selep.getNotDespierto(epi.ini, epi.fin)
            print "Despierto intervalo", epi.ini, epi.fin, "en:", desp
            return desp
            
        if(ep1):
            print "Actualizar episodio izquierdo"
            idx = self.cbx1.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, temperatura=True)
            self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, flujo=True)
            self.plotGraph(self.fig1_var3, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, consumo=True)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = self.cbx2.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, temperatura=True)
            self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, flujo=True)
            self.plotGraph(self.fig2_var3, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, consumo=True)
    
    def plotGraph(self, fig, tiempo, data, despierto, temperatura=False, flujo=False, consumo=False):
        ax = fig.axes[0]
        ax.clear()
        if(temperatura):
            ax.set_ylabel('Temperatura (ºC)', color=colores.temperatura)
            ax.set_ylim([25,40])
            color = colores.temperatura
        elif(flujo):
            ax.set_ylabel('Flujo térmico', color=colores.flujo)
            ax.set_ylim([-20,220])
            color = colores.flujo
        elif(consumo):
            ax.set_ylabel('Consumo (cal)', color=colores.consumo)
            ax.set_ylim([5,20])
            color = colores.consumo

        ax.plot(tiempo, data, color)
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        start, end = ax.get_xlim()
        ax.grid(True)
        
        #Lineas verticales con la clasificación de sueños
        for i in despierto:
            ax.axvspan(i[0], i[1], facecolor=colores.despierto, alpha=0.5, edgecolor=colores.despierto)
            
        fig.canvas.draw()
        
    def plotDendrogram(self, c1, c2):
        fig, self.axes = plt.subplots(1, 1, figsize=(8, 3), tight_layout=True)
        if(self.rbTemperatura.isChecked()):
            dn1 = dendrogram(c1.Z, ax=self.axes, leaf_rotation=20., labels=c1.labels)
            self.axes.set_title("Dendrograma de temperatura y flujo")
        elif(self.rbConsumo.isChecked()):
            dn2 = dendrogram(c2.Z, ax=self.axes, leaf_rotation=20., labels=c2.labels)
            self.axes.set_title("Dendrograma de consumo")
        return FigureCanvas(fig)
        
    def initCluster(self):
        self.cluster_tf = clustering.HierarchicalClustering(self.selep, tf=True)
        self.cluster_cons = clustering.HierarchicalClustering(self.selep, cons=True)
        
        #self.canvasCluster_tf = FigureCanvas(self.plotDendrogram(self.cluster_tf))
        #self.canvasCluster_cons = FigureCanvas(self.plotDendrogram(self.cluster_cons))
        
        #self.dendogramLayout.addWidget(self.canvasCluster_tf)
        #self.dendogramLayout.addWidget(self.canvasCluster_cons)
        
        self.dendogramLayout.addWidget(self.plotDendrogram(self.cluster_tf, self.cluster_cons))
        """
        self.fc = plt.figure()
        self.fc.add_subplot(111)
        self.canvasCluster = FigureCanvas(self.fc)
        """
        
        
    #Mejorar con hide/show
    def cluster(self, consumo=False):
        print "Mostrar dendograma y distancias"
        for cnt in reversed(range(self.tableLayout.count())):
            widget = self.tableLayout.takeAt(cnt).widget()
            if widget is not None:
                widget.deleteLater()
        for cnt in reversed(range(self.dendogramLayout.count())):
            widget = self.dendogramLayout.takeAt(cnt).widget()
            if widget is not None:
                widget.deleteLater()
        """    
        self.dendogramLayout.removeWidget(self.canvasCluster)
        self.canvasCluster.close()
        """
        
        self.dendogramLayout.addWidget(self.plotDendrogram(self.cluster_tf, self.cluster_cons))
        
        if(self.rbTemperatura.isChecked()):
            #self.canvasCluster_tf.show()
            #self.canvasCluster_cons.hide()
            self.tableLayout.addWidget(self.createTable(self.cluster_tf.distancias))
        elif(self.rbConsumo.isChecked()):
            #self.canvasCluster_tf.hide()
            #self.canvasCluster_cons.show()
            self.tableLayout.addWidget(self.createTable(self.cluster_cons.distancias))
        
    def createTable(self, clusters):
        horHeaders = []
        for i in range(len(self.selep.epFiltro)):
            horHeaders.append(str(i+1))
        table = MyTable(clusters, len(clusters), len(clusters))
        table.setHorizontalHeaderLabels(horHeaders)
        table.setVerticalHeaderLabels(horHeaders)
        return table
        
    def cbx1Listener(self, text):
        print "Episodio izquierdo", text   
        self.updatePlots(ep1=True)
        
    def cbx2Listener(self, text):
        print "Episodio derecho", text
        self.updatePlots(ep2=True)
    
    #Selecciona los individuos a agrupar
    def rbListener(self):
        print "Radio button"
        self.axes.clear()
        self.cluster()
        
    
                
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    
    sys.exit(app.exec_())
    
    
