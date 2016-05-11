# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
import cachitos
import colores
import leeFichero

DEBUG = 1

Ui_MainWindow, QMainWindow = loadUiType('int_consumos.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        
        if(DEBUG): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        
        print "Abriendo fichero ", fname
        self.selep = cachitos.selEpisodio(fname, dias=True)
        
        self.initCombobox()
        self.initGraphs()
        self.plotGraph(self.fig_izq, self.cbx_izq.currentIndex())
        self.plotGraph(self.fig_der, self.cbx_der.currentIndex())
        self.plotBarDiario()
        
        self.cbx_izq.activated[str].connect(self.cbxIzqListener)
        self.cbx_der.activated[str].connect(self.cbxDerListener)
    
    def initCombobox(self):
        for i in range(len(self.selep.epsDias)):
            self.cbx_izq.addItem("Día " + str(i+1))
            self.cbx_der.addItem("Día " + str(i+1))
    
    def initGraphs(self):
        print "Inicializar gráficas"
        #Gráfico de barras diario
        self.fig_barDiario = plt.figure(tight_layout=True)
        self.fig_barDiario.add_subplot(111)
        canvas_diario = FigureCanvas(self.fig_barDiario)
        self.layout_diario.addWidget(canvas_diario)
        
        #Gráficas día izquierdo
        self.fig_izq = plt.figure(tight_layout=True)
        self.canvas_izq = FigureCanvas(self.fig_izq)
        self.layout_dia_izq.addWidget(self.canvas_izq)
        
        #Gráficas día derecho
        self.fig_der = plt.figure(tight_layout=True)
        canvas_der = FigureCanvas(self.fig_der)
        self.layout_dia_der.addWidget(canvas_der)
        
    def plotGraph(self, fig, cbx_idx):
        labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada']
        colors = [colores.sueno, colores.sedentario, colores.ligero, colores.moderado]
        #Gráfica de tiempos
        sizes = self.getSizes(cbx_idx, tiempo=True)
        ax_tiempo = fig.add_subplot(221)
        pie = ax_tiempo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        ax_tiempo.legend(pie[0], labels, loc="upper left", prop={'size':7})
        ax_tiempo.axis('equal')
        
        #Gráfica de consumos
        sizes = self.getSizes(cbx_idx, consumo=True)
        ax_consumo = fig.add_subplot(222)
        pie = ax_consumo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        #ax_consumo.legend(pie[0], labels, loc="upper left")
        ax_consumo.axis('equal')
        
        #Gráfica de ratios
        ax_bar= fig.add_subplot(212)
        
        ratios = []
        #ind = self.cbx_izq.currentIndex()
        for i in self.selep.epsDias[cbx_idx]:
            ratios.append(i.numCalorias / (i.fin - i.ini))
    
        self.plotRatioBar(ax_bar, cbx_idx, ratios)
    
    def getSizes(self, idx, tiempo=False, consumo=False):
        sizes = [0, 0, 0, 0]
        if(tiempo):
            # Calcular tiempo por actividad
            for i in self.selep.epsDias[idx]:
                if(i.tipo == cachitos.tipoSueno):
                    sizes[0] += len(i.tiempo)
                elif(i.tipo == cachitos.tipoSedentario):
                    sizes[1] += len(i.tiempo)
                elif(i.tipo == cachitos.tipoLigera):
                    sizes[2] += len(i.tiempo)
                elif(i.tipo == cachitos.tipoModerado):
                    sizes[3] += len(i.tiempo)
        elif(consumo):
            # Calcular calorías consumidas por actividad
            for i in self.selep.epsDias[idx]:
                if(i.tipo == cachitos.tipoSueno):
                    sizes[0] += i.numCalorias
                elif(i.tipo == cachitos.tipoSedentario):
                    sizes[1] += i.numCalorias
                elif(i.tipo == cachitos.tipoLigera):
                    sizes[2] += i.numCalorias
                elif(i.tipo == cachitos.tipoModerado):
                    sizes[3] += i.numCalorias
        
        print sizes
        return sizes
    
    
    def plotRatioBar(self, ax, idx, means):
        def onpick(event):
            rect = event.artist
            for i in range(len(bar)): #MEJORAR!!
                if (bar[i] == rect):
                    print "Barra", i, self.selep.epsDias[idx][i].nombre, self.selep.epsDias[idx][i].numCalorias, 'calorías', len(self.selep.epsDias[idx][i].tiempo), 'minutos'
                    #lbl = '(' + self.selep.epFiltro[i].nombre + ') ' + str(self.selep.epFiltro[i].numCalorias)[:6] + ' calorías ' + str(len(self.selep.epFiltro[i].tiempo)) + ' minutos'
                    #self.lblDetalles.setText(lbl)
                    return
                    
        colors = []
        for i in self.selep.epsDias[idx]:
            if(i.tipo == cachitos.tipoSueno):
                c = colores.sueno
            elif(i.tipo == cachitos.tipoSedentario):
                c = colores.sedentario
            elif(i.tipo == cachitos.tipoLigera):
                c = colores.ligero
            elif(i.tipo == cachitos.tipoModerado):
                c = colores.moderado
            colors.append(c)
        
        print len(means), "muestras"    
        ind = np.linspace(0, len(means), endpoint=False, num=len(means))
        bar = ax.bar(ind, means, color=colors, picker=1, align='center')
        ax.set_xticklabels(np.arange(len(means)))
        #fig.tight_layout()
        
        #canvas = FigureCanvas(fig)
        #vbox = QtGui.QGridLayout()
        #vbox.addWidget(canvas)
        #canvas.mpl_connect('pick_event', onpick)
        self.canvas_izq.mpl_connect('pick_event', onpick)
    
    
    def plotBarDiario(self):
        suenos = np.empty(len(self.selep.epsDias))
        sedentarias = np.empty(len(self.selep.epsDias))
        ligeras = np.empty(len(self.selep.epsDias))
        moderadas = np.empty(len(self.selep.epsDias))
        idx = 0
        for j in self.selep.epsDias:
            for i in j:
                if(i.tipo == cachitos.tipoSueno):
                    suenos[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoSedentario):
                    sedentarias[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoLigera):
                    ligeras[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoModerado):
                    moderadas[idx] += i.numCalorias
            idx += 1
        print suenos    
        print suenos + sedentarias
        ind = np.arange(len(self.selep.epsDias))
        self.fig_barDiario.axes[0].bar(ind, suenos, color=colores.sueno)
        self.fig_barDiario.axes[0].bar(ind, sedentarias, bottom=suenos, color=colores.sedentario)
        self.fig_barDiario.axes[0].bar(ind, ligeras, bottom=suenos+sedentarias, color=colores.ligero)
        self.fig_barDiario.axes[0].bar(ind, moderadas, bottom=suenos+sedentarias+ligeras, color=colores.moderado)
        
    def cbxIzqListener(self):
        print "Combobox izquierdo"
        print "axes: ", len(self.fig_izq.axes)
        for i in self.fig_izq.axes:
            i.clear()
        self.plotGraph(self.fig_izq, self.cbx_izq.currentIndex())
        self.fig_izq.canvas.draw()
    
    def cbxDerListener(self):
        print "Combobox derecho"
        print "axes: ", len(self.fig_der.axes)
        for i in self.fig_der.axes:
            i.clear()
        self.plotGraph(self.fig_der, self.cbx_der.currentIndex())
        self.fig_der.canvas.draw()
    
    
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
