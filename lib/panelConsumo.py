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
import lectorFichero as lf
import colores
import hover
import datetime 
import cachitos
from time import mktime
from datetime import datetime

DEBUG = 1


class PanelConsumo():
    def __init__(self, epsDias, layout_diario, layout_dia_izq, layout_dia_der, cbx_izq, cbx_der, lbl_izq, lbl_der):
        print "init"
        #Inicializar comoponentes
        self.epsDias = epsDias
        self.layout_diario = layout_diario
        self.layout_dia_izq = layout_dia_izq
        self.layout_dia_der = layout_dia_der
        self.cbx_izq = cbx_izq
        self.cbx_der = cbx_der
        self.lbl_izq = lbl_izq
        self.lbl_der = lbl_der
        
        #Inicializar gráficas
        self.initGraphs()
        self.loadData(epsDias)
        
        self.cbx_izq.activated[str].connect(self.cbxIzqListener)
        self.cbx_der.activated[str].connect(self.cbxDerListener)
    
    def loadData(self, epsDias):
        self.epsDias = epsDias
        
                
        self.initCombobox()
        self.plotGraph(self.fig_izq, self.cbx_izq.currentIndex())
        self.plotGraph(self.fig_der, self.cbx_der.currentIndex())
        self.plotBarDiario()
        
        self.setLabel(izq=True)
        self.setLabel(izq=False)
    
    
    def initCombobox(self):
        self.ldias = []
        self.cbx_izq.clear()
        self.cbx_der.clear()
        for i in self.epsDias:
            self.cbx_izq.addItem("Día " + str(i.epFiltro[0].tiempo[0].day))
            self.cbx_der.addItem("Día " + str(i.epFiltro[0].tiempo[0].day))
            self.ldias.append("Día " + str(i.epFiltro[0].tiempo[0].day))
        if(len(self.epsDias) > 1):
            self.cbx_der.setCurrentIndex(1)
            
    def initGraphs(self):
        print "Inicializar gráficas"
        #Gráfico de barras diario
        self.fig_barDiario = plt.figure()
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
        
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                return '{p:1.1f}%  ({v:d})'.format(p=pct,v=val)
            return my_autopct
        
        for i in fig.axes:
            i.clear()
        
        def make_picker(fig, wedges, texts):
            def onclick(event):
                wedge = event.artist
                label = wedge.get_label()
                print label
            # Make wedges selectable
            for wedge in wedges:
                wedge.set_picker(True)
            fig.canvas.mpl_connect('pick_event', onclick)

        
        
        #labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada']
        colors = [colores.sueno, colores.sedentario, colores.ligero, colores.moderado]
        #Gráfica de tiempos
        sizes = self.getSizes(cbx_idx, tiempo=True)
        ax_tiempo = fig.add_subplot(221)
        wedges, plt_labels, autotexts = ax_tiempo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        #make_picker(fig, wedges, autotexts)
        #ax_tiempo.legend(pie[0], labels, loc="upper left", prop={'size':7})
        ax_tiempo.axis('equal')
        ax_tiempo.set_title('Tiempo por actividad')
        
        #Gráfica de consumos
        sizes = self.getSizes(cbx_idx, consumo=True)
        ax_consumo = fig.add_subplot(222)
        pie = ax_consumo.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        #ax_consumo.legend(pie[0], labels, loc="upper left")
        ax_consumo.axis('equal')
        ax_consumo.set_title('Consumo por actividad')
        
        #Gráfica de ratios
        ax_bar= fig.add_subplot(212)
        ax_bar.locator_params(nbins=12)
        
        ratios = []
        #ind = self.cbx_izq.currentIndex()
        for i in self.epsDias[cbx_idx].epFiltro:
            ratios.append(i.numCalorias / (i.fin - i.ini))
    
        self.plotRatioBar(ax_bar, cbx_idx, ratios)
        
        fig.canvas.draw()
        #fig.canvas.mpl_connect('pick_event', self.onpick)
    
    def getSizes(self, idx, tiempo=False, consumo=False):
        sizes = [0, 0, 0, 0]
        if(tiempo):
            # Calcular tiempo por actividad
            for i in self.epsDias[idx].epFiltro:
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
            for i in self.epsDias[idx].epFiltro:
                if(i.tipo == cachitos.tipoSueno):
                    sizes[0] += i.numCalorias
                elif(i.tipo == cachitos.tipoSedentario):
                    sizes[1] += i.numCalorias
                elif(i.tipo == cachitos.tipoLigera):
                    sizes[2] += i.numCalorias
                elif(i.tipo == cachitos.tipoModerado):
                    sizes[3] += i.numCalorias
        if(DEBUG>2):
            print sizes
        return sizes
    
    def onpick(self, event):
        print "picado"
        """
        rect = event.artist
        for i in range(len(bar)): #MEJORAR!!
            if (bar[i] == rect):
                print "Barra", i, self.selep.epsDias[idx][i].nombre, self.selep.epsDias[idx][i].numCalorias, 'calorías', len(self.selep.epsDias[idx][i].tiempo), 'minutos'
                #lbl = '(' + self.selep.epFiltro[i].nombre + ') ' + str(self.selep.epFiltro[i].numCalorias)[:6] + ' calorías ' + str(len(self.selep.epFiltro[i].tiempo)) + ' minutos'
                #self.lblDetalles.setText(lbl)
                return
        """
    """
    means. medidas de las barras
    idx. indice del día
    """
    def plotRatioBar(self, ax, idx, means):
                    
        colors = []
        labels = []
        for i in self.epsDias[idx].epFiltro:
            if(i.tipo == cachitos.tipoSueno):
                c = colores.sueno
            elif(i.tipo == cachitos.tipoSedentario):
                c = colores.sedentario
            elif(i.tipo == cachitos.tipoLigera):
                c = colores.ligero
            elif(i.tipo == cachitos.tipoModerado):
                c = colores.moderado
            colors.append(c)
            labels.append(i.tiempo[0].strftime('%H:%M'))
            #labels.append(i.tiempo[0])
        
        print len(means), "muestras"
        if(DEBUG>2):
            print means
        
        
        #ind = np.linspace(0, len(means), endpoint=False, num=len(means))
        #bar = ax.bar(ind, means, color=colors, picker=1)
        
        #Mejorar
        r=[]
        for i in range(len(labels)):
            p, q = [], []
            p.append(mktime(datetime.strptime(labels[i], "%H:%M").timetuple())) 
            r.append(mktime(datetime.strptime(labels[i], "%H:%M").timetuple()))
            q.append(means[i])
            markerline, stemlines, baseline = ax.stem(p, q)
            plt.setp(markerline, 'markerfacecolor', colors[i])
            plt.setp(stemlines, 'color', colors[i])
        
        
        ax.set_xticks(r)
        ax.set_xticklabels(labels, rotation=90, fontsize=10)
        ax.set_title('Ratio consumo por minuto')
        ax.set_ylim(0, 15)
        
        if(DEBUG): 
            print self.epsDias[idx].epFiltro[0].tiempo[0], self.epsDias[idx].epFiltro[-1].tiempo[-1]
            #print labels
        #ax.set_xlim([self.epsDias[idx].epFiltro[0].tiempo[0], self.epsDias[idx].epFiltro[-1].tiempo[-1]])
        
        #cursor = hover.FollowDotCursor(ax, ind, means, tolerance=20)
        
        #fig.tight_layout()
        
        #canvas = FigureCanvas(fig)
        #vbox = QtGui.QGridLayout()
        #vbox.addWidget(canvas)
        #canvas.mpl_connect('pick_event', onpick)
        #self.canvas_izq.mpl_connect('pick_event', onpick)
    
    
    def plotBarDiario(self):
        self.fig_barDiario.axes[0].clear()
        
        suenos = np.empty(len(self.epsDias))
        sedentarias = np.empty(len(self.epsDias))
        ligeras = np.empty(len(self.epsDias))
        moderadas = np.empty(len(self.epsDias))
        idx = 0
        for j in self.epsDias:
            for i in j.epFiltro:
                if(i.tipo == cachitos.tipoSueno):
                    suenos[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoSedentario):
                    sedentarias[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoLigera):
                    ligeras[idx] += i.numCalorias
                elif(i.tipo == cachitos.tipoModerado):
                    moderadas[idx] += i.numCalorias
            idx += 1
        ind = np.arange(len(self.epsDias))
        self.fig_barDiario.axes[0].bar(ind, suenos, 0.8, color=colores.sueno, align='center', label='Dormido')
        self.fig_barDiario.axes[0].bar(ind, sedentarias, 0.8, bottom=suenos, color=colores.sedentario, align='center', label='Sedentario')
        self.fig_barDiario.axes[0].bar(ind, ligeras, 0.8, bottom=suenos+sedentarias, color=colores.ligero, align='center', label='Act. Ligera')
        self.fig_barDiario.axes[0].bar(ind, moderadas, 0.8, bottom=suenos+sedentarias+ligeras, color=colores.moderado, align='center', label='Act. Moderada')
        self.fig_barDiario.axes[0].set_xticks(ind)
        self.fig_barDiario.axes[0].set_xticklabels(self.ldias)
        self.fig_barDiario.axes[0].set_title('Consumo diario por actividades')
        self.fig_barDiario.axes[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
        self.fig_barDiario.subplots_adjust(bottom=0.2)

        self.fig_barDiario.canvas.draw()
        
    def cbxIzqListener(self):
        print "Combobox izquierdo"
        print "axes: ", len(self.fig_izq.axes)
        self.plotGraph(self.fig_izq, self.cbx_izq.currentIndex())
        self.setLabel(izq=True)
    
    def cbxDerListener(self):
        print "Combobox derecho"
        print "axes: ", len(self.fig_der.axes)
        self.plotGraph(self.fig_der, self.cbx_der.currentIndex())
        self.setLabel(izq=False)    
        
    def setLabel(self, izq):
        if(izq):
            self.lbl_izq.setText('Comienzo: ' + self.epsDias[self.cbx_izq.currentIndex()].epFiltro[0].tiempo[0].strftime('%H:%M %d-%m-%y') + "\n" + str(int(self.epsDias[self.cbx_izq.currentIndex()].totalCal)) + " calorías")
        else:
            self.lbl_der.setText('Comienzo: ' + self.epsDias[self.cbx_der.currentIndex()].epFiltro[0].tiempo[0].strftime('%H:%M %d-%m-%y') + "\n" + str(int(self.epsDias[self.cbx_der.currentIndex()].totalCal)) + " calorías")
     
        