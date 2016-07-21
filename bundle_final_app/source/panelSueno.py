# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
#sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as md
import colores
import clustering
from scipy.cluster.hierarchy import dendrogram
from tablaDistancias import TablaDistancias

DEBUG = 0


class PanelSueno():
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
        self.figTop = plt.figure(tight_layout=True)
        canvasTop = FigureCanvas(self.figTop)
        self.layTop.addWidget(canvasTop);
        #Graficas inferior
        self.figBot = plt.figure(tight_layout=True)
        canvasBot = FigureCanvas(self.figBot)
        self.layBot.addWidget(canvasBot)
        
        
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
            self.plotGraph(self.figTop, self.selep.epFiltro[idx], desp, prof)
        if(ep2):
            print "Actualizar episodio derecho"
            idx = self.cbx2.currentIndex()
            desp = getDespierto(self.selep.epFiltro[idx])
            prof = getProfundo(self.selep.epFiltro[idx])
            self.plotGraph(self.figBot, self.selep.epFiltro[idx], desp, prof)
            
    
    def plotGraph(self, fig, filtro, despierto, profundo):
        
        for i in fig.axes:
            i.clear()
        tiempo = filtro.tiempo
        temperatura = filtro.temp
        flujo = filtro.flujo
        consumo = filtro.consumo
        
        axTemperatura = fig.add_subplot(131)
        axTemperatura.plot(tiempo, temperatura, colores.temperatura)
        axTemperatura.set_ylabel('Temperatura (ºC)', color=colores.temperatura)
        axTemperatura.set_ylim([25,40])
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        axTemperatura.xaxis.set_major_formatter(xfmt)
        start, end = axTemperatura.get_xlim()
        axTemperatura.grid(True)
        
        axFlujo = fig.add_subplot(132)
        axFlujo.plot(tiempo, flujo, colores.flujo)
        axFlujo.set_ylabel('Flujo térmico', color=colores.flujo)
        axFlujo.set_ylim([-20, 220])
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        axFlujo.xaxis.set_major_formatter(xfmt)
        start, end = axFlujo.get_xlim()
        axFlujo.grid(True)
        
        axConsumo = fig.add_subplot(133)
        axConsumo.plot(tiempo, consumo, colores.consumo)
        axConsumo.set_ylabel('Consumo (cal)', color=colores.consumo)
        axConsumo.set_ylim([0, 20])
        fig.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        axConsumo.xaxis.set_major_formatter(xfmt)
        start, end = axConsumo.get_xlim()
        axConsumo.grid(True)
        
        #Lineas verticales con la clasificación de sueños
        for i in profundo:
            axTemperatura.axvspan(i[0], i[1], facecolor=colores.suenoProfundo, alpha=0.3, edgecolor=colores.suenoProfundo)
            axFlujo.axvspan(i[0], i[1], facecolor=colores.suenoProfundo, alpha=0.3, edgecolor=colores.suenoProfundo)
            axConsumo.axvspan(i[0], i[1], facecolor=colores.suenoProfundo, alpha=0.3, edgecolor=colores.suenoProfundo)
            
        for i in despierto:
            axTemperatura.axvspan(i[0], i[1], facecolor=colores.despierto, alpha=0.5, edgecolor=colores.despierto)
            axFlujo.axvspan(i[0], i[1], facecolor=colores.despierto, alpha=0.5, edgecolor=colores.despierto)
            axConsumo.axvspan(i[0], i[1], facecolor=colores.despierto, alpha=0.5, edgecolor=colores.despierto)
            
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
        table = TablaDistancias(clusters, len(clusters)-1, len(clusters)-1)
        table.setHorizontalHeaderLabels([self.selep.epFiltro[i].nombre for i in range(0, len(self.selep.epFiltro)-1)])
        table.setVerticalHeaderLabels([self.selep.epFiltro[i].nombre for i in range(1, len(self.selep.epFiltro))])
        table.resizeColumnsToContents()

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
    
