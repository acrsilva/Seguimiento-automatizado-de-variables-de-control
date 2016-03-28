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
    
    def crearWidget(self, filtro):
        fig10, fig11 = self.creaFiguras(filtro.tiempo, filtro.temp, filtro.flujo)
        canvas1 = FigureCanvas(fig10)
        canvas2 = FigureCanvas(fig11)
        vbox = QtGui.QGridLayout()
        vbox.addWidget(QtGui.QLabel("<b>Episodio:</b> " + filtro.tipo))
        vbox.addWidget(QtGui.QLabel("<b>Inicio:</b> " + str(filtro.tiempo[0])))
        vbox.addWidget(QtGui.QLabel("<b>Final:</b> " + str(filtro.tiempo[-1])))
        vbox.addWidget(QtGui.QLabel("<b>Duración:</b> %i min" % (len(filtro.tiempo))))
        vbox.addWidget(QtGui.QLabel("<b>Coeficiente de correlación:</b> " + str(filtro.correlacion)[:5]))
        vbox.addWidget(canvas1)
        vbox.addWidget(canvas2)
        return vbox
    
    #Inserta elementos en el layout con los nuevos episodios
    def updateView(self):
        if(len(self.selep.epFiltro) > 0):
            filtro = self.selep.epFiltro[self.epActual]
            self.vbox = self.crearWidget(filtro)
            self.layoutMatplot1.addLayout(self.vbox)
            if(len(self.selep.epFiltro) > 1):
                filtro = self.selep.epFiltro[self.epActual+1]
                self.vbox2 = self.crearWidget(filtro)
                self.layoutMatplot1.addLayout(self.vbox2)
                
                
    #Elimina el contenido del layout actual        
    def limpiarLayout(self):
        for cnt in reversed(range(self.vbox.count())):
            widget = self.vbox.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater() 
        for cnt in reversed(range(self.vbox2.count())):
            widget = self.vbox2.takeAt(cnt).widget()
            if widget is not None: 
                widget.deleteLater()
    
    #Comprueba que los episodios no salgan del rango
    def setBounds(self):
        if(self.epActual > len(self.selep.epFiltro)-2):
            self.epActual = len(self.selep.epFiltro)-2
            
    def filtrarSueno(self):
        print "Filtrar sueño"
        self.selep.filSueno = self.cbSueno.isChecked() #Cambiar el filtro
        self.selep.update() #Actualizar el array de episodios filtrados
        self.setBounds()
        self.limpiarLayout() 
        self.updateView() 
        
    def filtrarSedentario(self):
        print "Filtrar sedentario"
        self.selep.filSedentario = self.cbSedentario.isChecked()
        self.selep.update()
        self.setBounds()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarLigera(self):
        print "Filtrar ligera"
        self.selep.filLigero = self.cbLigera.isChecked()
        self.selep.update()
        self.setBounds()
        self.limpiarLayout()
        self.updateView()
        
    def filtrarModerada(self):
        print "Filtrar moderada"
        self.selep.filModerado = self.cbModerada.isChecked()
        self.selep.update()
        self.setBounds()
        self.limpiarLayout()
        self.updateView()
    
    def retroceder(self):
        if (self.epActual > 0):
            self.epActual -= 1
        print "episodio", self.epActual
        self.limpiarLayout()
        self.updateView()
        
    def avanzar(self):
        if (self.epActual < len(self.selep.epFiltro) - 2):
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
    
    
