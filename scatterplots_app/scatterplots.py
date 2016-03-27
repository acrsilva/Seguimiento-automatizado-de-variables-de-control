# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import episodios    
    
Ui_MainWindow, QMainWindow = loadUiType('scatterplots.ui')

    
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.eps = episodios.Episodios() #Obtener el selector de episodios
        
        self.updateView()
        
        self.cbSueno.clicked.connect(self.filtrarSueno)
        self.cbSedentario.clicked.connect(self.filtrarSedentario)
        self.cbLigera.clicked.connect(self.filtrarLigera)
        self.cbModerada.clicked.connect(self.filtrarModerada)
        self.btnPrev.clicked.connect(self.retroceder)
        self.btnNext.clicked.connect(self.avanzar)
    
    def creaFiguras(self, t, a, b):
        #Serie temporal
        fig0 = Figure()
        #Escala temperaturas
        ax1 = fig0.add_subplot(111)
        ax1.plot(t, a, 'b-')
        ax1.set_xlabel('tiempo (m)')
        ax1.set_ylabel('Temperatura (ºC)', color='b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')
        #Escala flujo térmico
        ax2 = ax1.twinx()
        ax2.plot(t, b, 'r-')
        ax2.set_ylabel('Flujo térmico', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
        
        #Scatterplot
        fig1 = Figure()
        ax1f1 = fig1.add_subplot(111)
        ax1f1.scatter(a, b)
        
        return fig0, fig1
    
    def updateView(self):
        fig10, fig11 = self.creaFiguras(self.eps.tiempo1, self.eps.temp1, self.eps.flujo1)
        fig20, fig21 = self.creaFiguras(self.eps.tiempo2, self.eps.temp2, self.eps.flujo2)
        fig30, fig31 = self.creaFiguras(self.eps.tiempo3, self.eps.temp3, self.eps.flujo3)
        
        canvas1 = FigureCanvas(fig10)
        canvas2 = FigureCanvas(fig11)
        canvas3 = FigureCanvas(fig20)
        canvas4 = FigureCanvas(fig21)
        canvas5 = FigureCanvas(fig30)
        canvas6 = FigureCanvas(fig31)
        
        lbl1 = QtGui.QLabel(self.eps.lbl1)
        lbl2 = QtGui.QLabel(self.eps.lbl2)
        lbl3 = QtGui.QLabel(self.eps.lbl3)
        
        vbox = QtGui.QGridLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(canvas1)
        vbox.addWidget(canvas2)
        
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(lbl2)
        vbox2.addWidget(canvas3)
        vbox2.addWidget(canvas4)
        
        vbox3 = QtGui.QVBoxLayout()
        vbox3.addWidget(lbl3)
        vbox3.addWidget(canvas5)
        vbox3.addWidget(canvas6)
        
        self.layoutMatplot1.addLayout(vbox)
        self.layoutMatplot1.addLayout(vbox2)
        self.layoutMatplot1.addLayout(vbox3)
            
    def addmpl(self, fig1, fig2):
        self.canvas = FigureCanvas(fig1)
        self.canvas2 = FigureCanvas(fig2)
        self.lbl1 = QtGui.QLabel("Tipo de actividad")
        self.layoutMatplot1.addWidget(self.lbl1)
        self.layoutMatplot1.addWidget(self.canvas)
        self.layoutMatplot1.addWidget(self.canvas2)
        self.canvas.draw()
    
    def filtrarSueno(self):
        if self.cbSueno.isChecked():
            print "mostrar clasificación sueno"
        else:
            print "ocultar clasificación sueno"
    
    def filtrarSedentario(self):
        if self.cbSedentario.isChecked():
            print "mostrar actividad sedentario"
        else:
            print "ocultar actividad sedentario"
    
    def filtrarLigera(self):
        if self.cbLigera.isChecked():
            print "mostrar actividad ligera"
        else:
            print "ocultar actividad ligera"
        
    def filtrarModerada(self):
        if self.cbModerada.isChecked():
            print "mostrar actividad moderada"
        else:
            print "ocultar actividad moderada"
    
    def retroceder(self):
        self.eps.epAnterior()
        
    def avanzar(self):
        self.eps.epSiguiente()
        
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
