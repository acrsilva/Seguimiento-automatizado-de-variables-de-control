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
import lectorFichero as lf
import colores
import clustering
from scipy.cluster.hierarchy import dendrogram
from datetime import datetime
import cachitos

DEBUG = 0
PRUEBAS=1



Ui_MainWindow, QMainWindow = loadUiType('int_estudio_sueno_nuevo.ui')

class TablaDiagonal(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.rellenar()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    #Rellena la diagonal inferior de la tabla y colorea la distancia menor de cada fila
    def rellenar(self):
        i = self.data.shape[0]-2
        while(i >= 0):
            j=i
            if(j==0): min = j
            else: min = j-1
            while(j >= 0):
                if(self.data[i+1][j] < self.data[i+1][min]): min = j
                self.setItem(i, j, QTableWidgetItem(format(self.data[i+1][j], '.1f')))
                j -= 1
            self.item(i,min).setBackground(QtGui.QColor(colores.marcatabla))
            i -= 1


class TabPane():
    def __init__(self, selep, layTop, layBot, cbx1, cbx2, rbTemperatura, rbConsumo, lbl1, lbl2, tableLayout, dendrogramLayout):
        self.layTop = layTop
        self.layBot = layBot
        self.cbx1 = cbx1
        self.cbx2 = cbx2
        self.rbTemperatura = rbTemperatura
        self.rbConsumo = rbConsumo
        self.lbl1 = lbl1
        self.lbl2 = lbl2
        self.tableLayout = tableLayout
        self.dendrogramLayout = dendrogramLayout
        
        self.cbx1.activated[str].connect(self.cbx1Listener)
        self.cbx2.activated[str].connect(self.cbx2Listener)
        self.rbTemperatura.clicked.connect(self.rbListener)
        self.rbConsumo.clicked.connect(self.rbListener)
        
        self.initGraphs()
        self.loadData(selep)
        
        
    def initGraphs(self):
        #Graficas superior
        self.fig1_var1 = plt.figure(tight_layout=True)
        self.fig1_var1.add_subplot(111)
        self.fig1_var2 = plt.figure(tight_layout=True)
        self.fig1_var2.add_subplot(111)
        self.fig1_var3 = plt.figure(tight_layout=True)
        self.fig1_var3.add_subplot(111)

        #Graficas inferior
        self.fig2_var1 = plt.figure(tight_layout=True)
        self.fig2_var1.add_subplot(111)
        self.fig2_var2 = plt.figure(tight_layout=True)
        self.fig2_var2.add_subplot(111)
        self.fig2_var3 = plt.figure(tight_layout=True)
        self.fig2_var3.add_subplot(111)
        
        
        
        self.layTop.addWidget(FigureCanvas(self.fig1_var1))
        self.layTop.addWidget(FigureCanvas(self.fig1_var2))
        self.layTop.addWidget(FigureCanvas(self.fig1_var3))
        self.layBot.addWidget(FigureCanvas(self.fig2_var1))
        self.layBot.addWidget(FigureCanvas(self.fig2_var2))
        self.layBot.addWidget(FigureCanvas(self.fig2_var3))
    
    #Carga un fichero de datos csv y obtiene los episodios de sueño
    #Inicializa el contenido de la interfaz
    def loadData(self, selep):
        self.selep = selep
        #print 'selep ', len(selep.epFiltro)
        self.configureComboBox()
        self.updatePlots(ep1=True, ep2=True)
        self.initCluster()
        self.cluster()
        self.setLabel(sup=True)
        self.setLabel(sup=False)
    
        
    #Añade los nombres de los episodios en los combobox de todas las pestañas
    def configureComboBox(self):
        print "Configurando combobox"
        self.cbx1.clear()
        self.cbx2.clear()
        
        eps = self.selep.epFiltro
        for i in range(len(eps)):
            self.cbx1.addItem(eps[i].nombre)
            self.cbx2.addItem(eps[i].nombre)
            
        if(len(eps) > 1):
            self.cbx2.setCurrentIndex(1)

    #Muestra la fecha y la hora del episodio seleccionado
    def setLabel(self, sup):
        if(sup):
            self.lbl1.setText(self.selep.epFiltro[self.cbx1.currentIndex()].tiempo[0].strftime('%d-%m-%y (%H:%M') +" - "+ self.selep.epFiltro[self.cbx1.currentIndex()].tiempo[-1].strftime('%H:%M)'))
        else:
            self.lbl2.setText(self.selep.epFiltro[self.cbx2.currentIndex()].tiempo[0].strftime('%d-%m-%y (%H:%M') +" - "+ self.selep.epFiltro[self.cbx2.currentIndex()].tiempo[-1].strftime('%H:%M)'))
    
    
    def updatePlots(self, ep1=False, ep2=False):
        """
        Actualiza el contenido de las gráficas con el episodio seleccionado por los combobox
        pest: pestaña selecciona
        ep1/ep2: episodio a actualizar, el superior y el inferior
        """
        def getDespierto(epi):
            desp = self.selep.getDespierto(epi.ini, epi.fin)
            if(DEBUG): print "Despierto intervalo", epi.ini, epi.fin, "en:", desp
            return desp
        
        def getProfundo(epi):
            prof = self.selep.getProfundo(epi.ini, epi.fin)
            if(DEBUG): print "Sueño profundo intervalo", epi.ini, epi.fin, "en:", prof
            return prof
            
        if(ep1):
            print "Actualizar episodio izquierdo"
            idx = self.cbx1.currentIndex()
            print len(self.selep.epFiltro), idx
            desp = getDespierto(self.selep.epFiltro[idx])
            prof = getProfundo(self.selep.epFiltro[idx])
            self.plotGraph(self.fig1_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, prof, temperatura=True)
            self.plotGraph(self.fig1_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, prof, flujo=True)
            self.plotGraph(self.fig1_var3, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, prof, consumo=True)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = self.cbx2.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            prof = getProfundo(self.selep.epFiltro[idx])
            self.plotGraph(self.fig2_var1, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, prof, temperatura=True)
            self.plotGraph(self.fig2_var2, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, prof, flujo=True)
            self.plotGraph(self.fig2_var3, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, prof, consumo=True)
        
    def plotGraph(self, fig, tiempo, data, despierto, profundo, temperatura=False, flujo=False, consumo=False):
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
            ax.set_ylim([0,20])
            color = colores.consumo

        ax.plot(tiempo, data, color)
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        start, end = ax.get_xlim()
        ax.grid(True)
        
        #Lineas verticales con la clasificación de sueños
        for i in profundo:
            ax.axvspan(i[0], i[1], facecolor=colores.suenoProfundo, alpha=0.3, edgecolor=colores.suenoProfundo)
            
        for i in despierto:
            ax.axvspan(i[0], i[1], facecolor=colores.despierto, alpha=0.5, edgecolor=colores.despierto)
            
        fig.canvas.draw()

    #Dibuja el dendrograma
    def plotDendrogram(self, c1, c2):
        fig, self.axes = plt.subplots(1, 1, figsize=(8, 3), tight_layout=True)
        if(self.rbTemperatura.isChecked()):
            dn1 = dendrogram(c1.Z, ax=self.axes, leaf_rotation=90., labels=c1.labels, leaf_font_size=10., )
            self.axes.set_title("Dendrograma de temperatura y flujo")
        elif(self.rbConsumo.isChecked()):
            dn2 = dendrogram(c2.Z, ax=self.axes, leaf_rotation=90., labels=c2.labels, leaf_font_size=10., )
            self.axes.set_title("Dendrograma de consumo")
            
        self.axes.set_xlabel('Episodios de sueño')
        self.axes.set_ylabel('Distancia')
        return FigureCanvas(fig)
    
    #Realiza el clustering de temperatura y flujo y de consumo y dibuja el dendrograma
    def initCluster(self):
        self.cluster_tf = clustering.HierarchicalClustering(self.selep, tf=True)
        self.cluster_cons = clustering.HierarchicalClustering(self.selep, cons=True)
        
        self.dendrogramLayout.addWidget(self.plotDendrogram(self.cluster_tf, self.cluster_cons))
       
        
    #Mejorar con hide/show
    def cluster(self, consumo=False):
        print "Mostrar dendrograma y distancias"
        for cnt in reversed(range(self.tableLayout.count())):
            widget = self.tableLayout.takeAt(cnt).widget()
            if widget is not None:
                widget.deleteLater()
        for cnt in reversed(range(self.dendrogramLayout.count())):
            widget = self.dendrogramLayout.takeAt(cnt).widget()
            if widget is not None:
                widget.deleteLater()
                
        self.dendrogramLayout.addWidget(self.plotDendrogram(self.cluster_tf, self.cluster_cons))
        
        if(self.rbTemperatura.isChecked()):
            self.tableLayout.addWidget(self.createTable(self.cluster_tf.distancias))
        elif(self.rbConsumo.isChecked()):
            self.tableLayout.addWidget(self.createTable(self.cluster_cons.distancias))
        
    def createTable(self, clusters):
        header = []
        for i in self.selep.epFiltro:
            header.append(i.nombre)
        table = TablaDiagonal(clusters, len(clusters)-1, len(clusters)-1)
        table.setHorizontalHeaderLabels([self.selep.epFiltro[i].nombre for i in range(0, len(self.selep.epFiltro)-1)])
        table.setVerticalHeaderLabels([self.selep.epFiltro[i].nombre for i in range(1, len(self.selep.epFiltro))])
        return table
        
    def cbx1Listener(self, text):
        print "Episodio izquierdo", text   
        self.updatePlots(ep1=True)
        self.setLabel(sup=True)

    def cbx2Listener(self, text):
        print "Episodio derecho", text
        self.updatePlots(ep2=True)
        self.setLabel(sup=False)
    
    def rbListener(self):
        """
        Selecciona los individuos a agrupar
        """
        print "Radio button"
        self.axes.clear()
        self.cluster()
    
        

# plotLayout
# cbx1, cbx2
# btnAbrir, btnClustering
# rbTemperatura, rbConsumo
# tableDistancias
# dendrogramLayout
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        #self.showMaximized()
        #Cargar el diseño de la interfaz del QtDesigner
        self.setupUi(self)
        
        #self.__initGraphs__()
        self.loadData()
        
        #Conectar elementos de la interfaz
        """
        self.cbx1.activated[str].connect(self.cbx1Listener)
        self.cbx2.activated[str].connect(self.cbx2Listener)
        self.rbTemperatura.clicked.connect(self.rbListener)
        self.rbConsumo.clicked.connect(self.rbListener)
        """
        self.actionAbrir.triggered.connect(self.loadData)
        self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.tabListener)
        
        print "Listo"
    
    def initTabs(self):
        self.tabs = []
        self.tabs.append(TabPane(self.selep, self.plotLayoutUp, self.plotLayoutBot, self.cbx1, self.cbx2, 
                            self.rbTemperatura, self.rbConsumo, self.lbl1, self.lbl2, self.tableLayout, self.dendrogramLayout))
        
        
        self.selep.update(sNocturno=False, sedentario=False, ligero=False, moderado=False)
        self.tabs.append(TabPane(self.selep, self.plotLayoutUpSiestas, self.plotLayoutBotSiestas, self.cbx1Siestas,
                            self.cbx2Siestas, self.rbTemperaturaSiestas, self.rbConsumoSiestas, self.lbl1Siestas,
                            self.lbl2Siestas, self.tableLayoutSiestas, self.dendrogramLayoutSiestas))
        
        self.selep.update(sDiurno=False, sedentario=False, ligero=False, moderado=False)
        self.tabs.append(TabPane(self.selep, self.plotLayoutUpSuenos, self.plotLayoutBotSuenos, self.cbx1Suenos,
                            self.cbx2Suenos, self.rbTemperaturaSuenos, self.rbConsumoSuenos, self.lbl1Suenos,
                            self.lbl2Suenos, self.tableLayoutSuenos, self.dendrogramLayoutSuenos))
        
    #Carga un fichero de datos csv y obtiene los episodios de sueño
    #Inicializa el contenido de la interfaz
    def loadData(self):
        if(PRUEBAS): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        csv = lf.LectorFichero(fname).getDatos()
        self.selep = cachitos.selEpisodio(csv, sedentario=False, ligero=False, moderado=False)
        
        self.setWindowTitle('Estudio de sueños (' + fname +')')
        
        self.initTabs()
        
        #self.configureComboBox()
        #self.updatePlots('todos', ep1=True, ep2=True)
        #self.initCluster()
        #self.cluster()
        #self.setLabel(sup=True)
        #self.setLabel(sup=False)
        

    #FALTA PASAR LA LISTA DE DIURNOS Y NOCTURNOS    
    def updatePlots(self, pest, ep1=False, ep2=False):
        """
        Actualiza el contenido de las gráficas con el episodio seleccionado por los combobox
        pest: pestaña selecciona
        ep1/ep2: episodio a actualizar, el superior y el inferior
        """
        def getDespierto(epi):
            desp = self.selep.getDespierto(epi.ini, epi.fin)
            if(DEBUG): print "Despierto intervalo", epi.ini, epi.fin, "en:", desp
            return desp
        
        def getProfundo(epi):
            prof = self.selep.getProfundo(epi.ini, epi.fin)
            if(DEBUG): print "Sueño profundo intervalo", epi.ini, epi.fin, "en:", prof
            return prof
        
        print self.tabWidget.currentIndex(), pest
        tab = self.tabWidget.currentIndex()
        #Todos los episodios
        if(tab == 0):
            cb1 = self.cbx1
            cb2 = self.cbx2
            f11 = self.fig1_var1
            f12 = self.fig1_var2
            f13 = self.fig1_var3
            f21 = self.fig2_var1
            f22 = self.fig2_var2
            f23 = self.fig2_var3
        #Episodios diurnos
        elif(tab == 1):
            cb1 = self.cbx1Siestas
            cb2 = self.cbx2Siestas
        #Episodios nocturnos
        elif(tab == 2):
            cb1 = self.cbx1Suenos
            cb2 = self.cbx2Suenos
            
        if(ep1):
            print "Actualizar episodio izquierdo"
            idx = cb1.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            prof = getProfundo(self.selep.epFiltro[idx])
            self.plotGraph(f11, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, prof, temperatura=True)
            self.plotGraph(f12, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, prof, flujo=True)
            self.plotGraph(f13, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, prof, consumo=True)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = cb2.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            prof = getProfundo(self.selep.epFiltro[idx])
            self.plotGraph(f21, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].temp, desp, prof, temperatura=True)
            self.plotGraph(f22, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].flujo, desp, prof, flujo=True)
            self.plotGraph(f23, self.selep.epFiltro[idx].tiempo, self.selep.epFiltro[idx].consumo, desp, prof, consumo=True)
            
                
    def tabListener(self):
        curTab = self.tabWidget.currentIndex()
        print "Tab ", curTab
        #self.tabs[curTab].loadData(self.
        
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    
    sys.exit(app.exec_())
    
    
