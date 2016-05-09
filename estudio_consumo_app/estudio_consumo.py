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

Ui_MainWindow, QMainWindow = loadUiType('int_consumos.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.selep = cachitos.selEpisodio("../data.csv", dias=True)
        
        self.__initCombobox__()
        self.initGraphs()
        self.plotGraph(izq=True)
        self.plotBarDiario()
        
        #self.drawActividadesPie()
        #self.drawConsumosPie()
        #self.drawRatioBar()
        
        self.cbx_izq.activated[str].connect(self.cbxIzqListener)
    
    def __initCombobox__(self):
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
        
    def plotGraph(self, izq=False, der=False):
        if(izq):
            labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada']
            colors = [colores.sueno, colores.sedentario, colores.ligero, colores.moderado]
            #Gráfica de tiempos
            sizes = self.getSizes(self.cbx_izq.currentIndex(), tiempo=True)
            ax_tiempo = self.fig_izq.add_subplot(221)
            pie = ax_tiempo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
            ax_tiempo.legend(pie[0], labels, loc="upper left", prop={'size':7})
            ax_tiempo.axis('equal')
            
            #Gráfica de consumos
            sizes = self.getSizes(self.cbx_izq.currentIndex(), consumo=True)
            ax_consumo = self.fig_izq.add_subplot(222)
            pie = ax_consumo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
            #ax_consumo.legend(pie[0], labels, loc="upper left")
            ax_consumo.axis('equal')
            
            #Gráfica de ratios
            ax_bar= self.fig_izq.add_subplot(212)
            
            ratios = []
            idx = self.cbx_izq.currentIndex()
            for i in self.selep.epsDias[idx]:
                ratios.append(i.numCalorias / (i.fin - i.ini))
        
            self.plotRatioBar(ax_bar, idx, ratios)
    
    def plotBarDiario(self):
        """
        suenos = [0]*len(self.selep.epsDias)
        sedentarias = [0]*len(self.selep.epsDias)
        ligeras = [0]*len(self.selep.epsDias)
        moderadas = [0]*len(self.selep.epsDias)
        """
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
        
            
    def __crearPieWidget__(self, sizes):
        #labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada', 'Act. Intensa', 'Act. Muy intensa']
        labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada']
        colors = [colores.sueno, colores.sedentario, colores.ligero, colores.moderado]
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111) 
        pie = ax.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        ax.legend(pie[0], labels, loc="upper left")
        ax.axis('equal')
        fig.tight_layout()

        return FigureCanvas(fig)
    
    
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
    
    
    def __crearBarWidget__(self, means):
        def onpick(event):
            rect = event.artist
            for i in range(len(self.bar)): #MEJORAR!!
                if (self.bar[i] == rect):
                    print "Barra", self.selep.epFiltro[i].nombre, self.selep.epFiltro[i].numCalorias, 'calorías', len(self.selep.epFiltro[i].tiempo), 'minutos'
                    lbl = '(' + self.selep.epFiltro[i].nombre + ') ' + str(self.selep.epFiltro[i].numCalorias)[:6] + ' calorías ' + str(len(self.selep.epFiltro[i].tiempo)) + ' minutos'
                    self.lblDetalles.setText(lbl)
                    return
                    
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        colors = []
        for i in self.selep.epFiltro:
            if(i.tipo == cachitos.tipoSueno):
                c = colores.sueno
            elif(i.tipo == cachitos.tipoSedentario):
                c = colores.sedentario
            elif(i.tipo == cachitos.tipoLigera):
                c = colores.ligero
            elif(i.tipo == cachitos.tipoModerado):
                c = colores.moderado
            colors.append(c)
            
        ind = np.linspace(10, len(means), num=len(means))
        self.bar = ax.bar(ind, means, color=colors, picker=1, align='center')
        ax.set_xticklabels(np.arange(len(means)))
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        vbox = QtGui.QGridLayout()
        vbox.addWidget(canvas)
        canvas.mpl_connect('pick_event', onpick)
        
        #return FigureCanvas(fig)
        return vbox
    
    def drawActividadesPie(self):
        print "Dibujar gráfica actividades"
        #sizes = [0, 0, 0, 0, 0, 0]
        sizes = [0, 0, 0, 0]
        # Calcular tiempo por actividad
        for i in self.selep.epFiltro:
            if(i.tipo == cachitos.tipoSueno):
                sizes[0] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoSedentario):
                sizes[1] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoLigera):
                sizes[2] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoModerado):
                sizes[3] += len(i.tiempo)
        print sizes
        
        self.layout_pie_tiempos.addWidget(self.__crearPieWidget__(sizes))

    def drawConsumosPie(self):
        print "Dibujar gráfica consumos"
        #sizes = [0, 0, 0, 0, 0, 0]
        sizes = [0, 0, 0, 0]
        # Calcular calorías consumidas por actividad
        for i in self.selep.epFiltro:
            if(i.tipo == cachitos.tipoSueno):
                sizes[0] += i.numCalorias
            elif(i.tipo == cachitos.tipoSedentario):
                sizes[1] += i.numCalorias
            elif(i.tipo == cachitos.tipoLigera):
                sizes[2] += i.numCalorias
            elif(i.tipo == cachitos.tipoModerado):
                sizes[3] += i.numCalorias
        print sizes
        
        self.layout_pie_consumos.addWidget(self.__crearPieWidget__(sizes))
        
    def drawRatioBar(self):
        print "Dibujar barra de ratios"
        # Calcular ratio calorias / minuto
        ratios = []
        for i in self.selep.epFiltro:
            ratios.append(i.numCalorias / (i.fin - i.ini))
        
        self.layout_bar_ratio.addLayout(self.__crearBarWidget__(ratios))
    
    def cbxIzqListener(self):
        print "Combobox izquierdo"
        print "axes: ", len(self.fig_izq.axes)
        for i in self.fig_izq.axes:
            i.clear()
        self.plotGraph(izq=True)
        self.fig_izq.canvas.draw()
    
    def cbxDerListener(self):
        print "Combobox derecho"
        self.plotGraph(der=True)
    
    
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
