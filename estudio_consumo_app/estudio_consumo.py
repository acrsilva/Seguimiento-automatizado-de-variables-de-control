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

Ui_MainWindow, QMainWindow = loadUiType('interfaz.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.selep = cachitos.selEpisodio("../data.csv")
        #self.totalEpisodios = len(self.selep.episodios)
        
        self.drawActividadesPie()
        
    def drawActividadesPie(self):
        print "Dibujar gráfica actividades"
        labels = ['Sedentario', 'Act. Ligera', 'Act. Moderada', 'Sueno']
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        sizes = [0, 0, 0, 0]
        #Falta calcular tiempos!!!!
        for i in self.selep.episodios:
            if(i.tipo == cachitos.tipoSueno):
                sizes[0] += 1
            elif(i.tipo == cachitos.tipoSedentario):
                sizes[1] += 1
            elif(i.tipo == cachitos.tipoLigera):
                sizes[2] += 1
            elif(i.tipo == cachitos.tipoModerado):
                sizes[3] += 1
        
        print sizes
         
        fig = plt.figure()
        ax = fig.add_subplot(111) 
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        
        self.pie_tiempo.canvas = FigureCanvas(fig)
        self.pie_tiempo.canvas.draw()

    def drawConsumosPie(self):
        print "Dibujar gráfica consumos"
        

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
