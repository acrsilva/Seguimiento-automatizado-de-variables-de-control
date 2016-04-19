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
        
        self.drawActividadesPie()
        #self.drawConsumosPie()
    
    def __crearWidget__(self, sizes):
        labels = ['Dormido', 'Sedentario', 'Act. Ligera', 'Act. Moderada', 'Act. Intensa', 'Act. Muy intensa']
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red', 'red'] #CAMBIAR COLORES!!!
        fig = plt.figure()
        #fig.suptitle("Tiempo por actividad", fontsize = 22)
        ax = fig.add_subplot(111) 
        pie = ax.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
        ax.legend(pie[0], labels, loc="best")
        ax.axis('equal')
        fig.tight_layout()
        
        return FigureCanvas(fig)
        
    def drawActividadesPie(self):
        print "Dibujar gráfica actividades"
        sizes = [0, 0, 0, 0, 0, 0]
        # Calcular tiempo de cada actividad
        for i in self.selep.episodios:
            if(i.tipo == cachitos.tipoSueno):
                sizes[0] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoSedentario):
                sizes[1] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoLigera):
                sizes[2] += len(i.tiempo)
            elif(i.tipo == cachitos.tipoModerado):
                sizes[3] += len(i.tiempo)
        print sizes
        
        self.layout_pie_tiempos.addWidget(self.__crearWidget__(sizes))

    def drawConsumosPie(self):
        print "Dibujar gráfica consumos"
        
        

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
