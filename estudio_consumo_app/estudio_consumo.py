# -*- coding: utf-8 -*-

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

Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')

class prueba:
    def __init__(self, num):
        self.num = num
        self.p = "clase prueba"

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.selep = cachitos.selEpisodio("../data.csv")
        
        self.drawActividadesPie()
        self.drawConsumosPie()
        self.drawRatioBar()
    
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
        
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
