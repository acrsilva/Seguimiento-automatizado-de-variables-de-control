# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import cachitos
import datetime
from matplotlib.dates import MinuteLocator
import matplotlib.dates as md
    
Ui_MainWindow, QMainWindow = loadUiType('scatterplots.ui')

    
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.epActual = 0
        
        self.selep = cachitos.selEpisodio() #Obtener el selector de episodios
        
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
        ax1.set_xlabel('Tiempo (m)')
        ax1.set_ylabel('Temperatura (ºC)', color='b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')
        fig0.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(xfmt) #Warning
        
        start, end = ax1.get_xlim()
        #ax1.xaxis.set_ticks(np.arange(start, end, 30))
        #ax1.grid(True)
        
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
    
    #Inserta elementos en el layout con los nuevos episodios
    def updateView(self):
        filtro = self.selep.epFiltro
        if(len(filtro) > 0):
            fig10, fig11 = self.creaFiguras(filtro[self.epActual].tiempo, filtro[self.epActual].temp, filtro[self.epActual].flujo)
            #fig20, fig21 = self.creaFiguras(self.selep.tiempo2, self.selep.temp2, self.selep.flujo2)
            #fig30, fig31 = self.creaFiguras(self.selep.tiempo3, self.selep.temp3, self.selep.flujo3)
            
            canvas1 = FigureCanvas(fig10)
            canvas2 = FigureCanvas(fig11)
            #canvas3 = FigureCanvas(fig20)
            #canvas4 = FigureCanvas(fig21)
            #canvas5 = FigureCanvas(fig30)
            #canvas6 = FigureCanvas(fig31)
            
            lbl1 = QtGui.QLabel("Episodio " + filtro[self.epActual].tipo)
            #lbl11 = QtGui.QLabel("Comienzo: " + str(self.selep.tiempo1[0]))
            #lbl12 = QtGui.QLabel("Fin: " + str(sel.eps.tiempo1[
            #lbl12 = QtGui.QLabel("Fin: ")
            #lbl13 = QtGui.QLabel("Duración: " + str(len(self.selep.tiempo1)))
            #lbl2 = QtGui.QLabel(self.selep.lbl2)
            #lbl3 = QtGui.QLabel(self.selep.lbl3)
            
            self.vbox = QtGui.QGridLayout()
            self.vbox.addWidget(QtGui.QLabel("Episodio " + filtro[self.epActual].tipo))
            self.vbox.addWidget(QtGui.QLabel("Comienzo " + str(filtro[self.epActual].ini)))
            #self.vbox.addWidget(lbl12)
            #self.vbox.addWidget(lbl13)
            self.vbox.addWidget(canvas1)
            self.vbox.addWidget(canvas2)
        
            """
            vbox2 = QtGui.QVBoxLayout()
            vbox2.addWidget(lbl2)
            vbox2.addWidget(canvas3)
            vbox2.addWidget(canvas4)
            
            vbox3 = QtGui.QVBoxLayout()
            vbox3.addWidget(lbl3)
            vbox3.addWidget(canvas5)
            vbox3.addWidget(canvas6)
            """
        
            self.layoutMatplot1.addLayout(self.vbox)
            #self.layoutMatplot1.addLayout(vbox2)
            #self.layoutMatplot1.addLayout(vbox3)
    
    #Elimina el contenido del layout actual        
    def limpiarLayout(self):
        for cnt in reversed(range(self.vbox.count())):
            widget = self.vbox.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater() 
            
    def filtrarSueno(self):
        print "Filtrar sueño"
        self.selep.filSueno = self.cbSueno.isChecked() #Cambiar el filtro
        self.selep.update() #Actualizar el array de episodios filtrados
        self.limpiarLayout() 
        self.updateView() 
        
    def filtrarSedentario(self):
        print "Filtrar sedentario"
        self.selep.filSedentario = self.cbSedentario.isChecked()
        self.selep.update()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarLigera(self):
        print "Filtrar ligera"
        self.selep.filLigero = self.cbLigera.isChecked()
        self.selep.update()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarModerada(self):
        print "Filtrar moderada"
        self.selep.filModerado = self.cbModerada.isChecked()
        self.selep.update()
        self.limpiarLayout()
        self.updateView()
    
    def retroceder(self):
        if (self.epActual > 0):
            self.epActual -= 1
        print "episodio", self.epActual
        self.limpiarLayout()
        self.updateView()
        
    def avanzar(self):
        if (self.epActual < len(self.selep.epFiltro) - 1):
            self.epActual += 1
        print "episodio", self.epActual
        self.limpiarLayout()
        self.updateView()
        
        
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
