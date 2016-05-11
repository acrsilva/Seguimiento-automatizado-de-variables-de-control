# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
sys.path.insert(0, '../lib')
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
#from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import cachitos
import matplotlib.dates as md
from sklearn import preprocessing

import scipy.spatial as spatial


DEBUG = 1


def fmt(x, y):
    return 'x: {x:0.2f}\ny: {y:0.2f}'.format(x=x, y=y)

class FollowDotCursor(object):
    """Display the x,y location of the nearest data point.
    http://stackoverflow.com/a/4674445/190597 (Joe Kington)
    http://stackoverflow.com/a/13306887/190597 (unutbu)
    http://stackoverflow.com/a/15454427/190597 (unutbu)
    """
    def __init__(self, ax, x, y, tolerance=5, formatter=fmt, offsets=(-20, 20)):
        try:
            x = np.asarray(x, dtype='float')
        except (TypeError, ValueError):
            x = np.asarray(md.date2num(x), dtype='float')
        y = np.asarray(y, dtype='float')
        mask = ~(np.isnan(x) | np.isnan(y))
        x = x[mask]
        y = y[mask]
        self._points = np.column_stack((x, y))
        self.offsets = offsets
        y = y[np.abs(y-y.mean()) <= 3*y.std()]
        self.scale = x.ptp()
        self.scale = y.ptp() / self.scale if self.scale else 1
        self.tree = spatial.cKDTree(self.scaled(self._points))
        self.formatter = formatter
        self.tolerance = tolerance
        self.ax = ax
        self.fig = ax.figure
        self.ax.xaxis.set_label_position('top')
        self.dot = ax.scatter(
            [x.min()], [y.min()], s=130, color='green', alpha=0.7)
        self.annotation = self.setup_annotation()
        plt.connect('motion_notify_event', self)

    def scaled(self, points):
        points = np.asarray(points)
        return points * (self.scale, 1)

    def __call__(self, event):
        print "a"
        ax = self.ax
        # event.inaxes is always the current axis. If you use twinx, ax could be
        # a different axis.
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
        elif event.inaxes is None:
            return
        else:
            inv = ax.transData.inverted()
            x, y = inv.transform([(event.x, event.y)]).ravel()
        annotation = self.annotation
        x, y = self.snap(x, y)
        annotation.xy = x, y
        annotation.set_text(self.formatter(x, y))
        self.dot.set_offsets((x, y))
        bbox = ax.viewLim
        event.canvas.draw()

    def setup_annotation(self):
        print "b"
        """Draw and hide the annotation box."""
        annotation = self.ax.annotate(
            '', xy=(0, 0), ha = 'right',
            xytext = self.offsets, textcoords = 'offset points', va = 'bottom',
            bbox = dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops = dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        return annotation

    def snap(self, x, y):
        print "c"
        """Return the value in self.tree closest to x, y."""
        dist, idx = self.tree.query(self.scaled((x, y)), k=1, p=1)
        try:
            return self._points[idx]
        except IndexError:
            # IndexError: index out of bounds
            return self._points[0]


    
Ui_MainWindow, QMainWindow = loadUiType('scatterplots.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.epActual = 0
        self.selep = self.loadData()
        #self.updateView()
        self.init_figures()
        self.updateFigures()
        
        self.cbSueno.clicked.connect(self.filtrarSueno)
        self.cbSedentario.clicked.connect(self.filtrarSedentario)
        self.cbLigera.clicked.connect(self.filtrarLigera)
        self.cbModerada.clicked.connect(self.filtrarModerada)
        self.btnPrev.clicked.connect(self.retroceder)
        self.btnNext.clicked.connect(self.avanzar)
        self.btnSelFile.clicked.connect(self.openFile)
        
        self.filSueno = True
        self.filSedentario = True
        self.filLigero =True
        self.filModerado = True
        
        
    def openFile(self):
        self.selep = self.loadData()
        self.limpiarLayout() 
        #self.updateView() 
    
    def loadData(self):
        if(DEBUG): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        selep = cachitos.selEpisodio(fname)
        return selep
    
    def init_figures(self):
        self.fig, self.ax = plt.subplots()
        canvas = FigureCanvas(self.fig)
        self.layoutMatplot1.addWidget(canvas)
        #canvas.mpl_connect('pick_event', lambda event: self.onpick(event, 1))
    
    def updateFigures(self):
        a = self.selep.epFiltro[self.epActual].temp
        b = self.selep.epFiltro[self.epActual].flujo
        self.ax.plot(a, b, 'o', picker=5)
        cursor = FollowDotCursor(self.ax, a, b, tolerance=0.5)
        
    
    def getTime(self, a, b, ep):
        for i in self.selep.epFiltro[self.epActual + ep].temp:
            if(a == i):
                ind = 0
                for k in self.selep.epFiltro[self.epActual + ep].flujo:
                    if(b == k):
                        print "encontrado"
                        return self.selep.epFiltro[self.epActual + ep].tiempo[ind]
                    else:
                        ind += 1
    
    def onpick(self, event, ep):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        print xdata[ind[0]], ydata[ind[0]]
        self.label.setText('Instante ' + str(self.getTime(xdata[ind[0]], ydata[ind[0]], ep)))
        
        self.ax.annotate(
            '', xy=(0, 0), ha = 'right',
            textcoords = 'offset points', va = 'bottom',
            bbox = dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=0.75),
            arrowprops = dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        
            
    def creaFiguras(self, t, a, b):
        #Serie temporal
        fig0 = plt.figure(tight_layout=True)
        #Normalizar
        preprocessing.scale(a, copy=True)
        preprocessing.scale(b, copy=True)
        #Curva temperatura
        ax1 = fig0.add_subplot(111)
        ax1.plot(t, a, 'b-')
        #ax1.set_ylim([-5,5])
        #ax1.set_xlabel('Tiempo (m)')
        ax1.set_ylabel('Temperatura (ºC)', color='b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')
        fig0.autofmt_xdate()
        xfmt = md.DateFormatter('%H:%M')
        ax1.xaxis.set_major_formatter(xfmt)
        
        start, end = ax1.get_xlim()
        #ax1.xaxis.set_ticks(np.arange(start, end, 30))
        ax1.grid(True)
        
        #Curva flujo térmico
        ax2 = ax1.twinx()
        ax2.plot(t, b, 'r-')
        #ax2.set_ylim([-5,5])
        ax2.set_ylabel('Flujo térmico', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
        
        #Scatterplot
        fig1 = plt.figure(tight_layout=True)
        ax1f1 = fig1.add_subplot(111)
        line, = ax1f1.plot(a, b, 'o', picker=5)
        #ax1f1.set_xlim([20,45])
        #ax1f1.set_ylim([-20,220])
        ax1f1.set_xlabel('Temperatura (ºC)', color='b')
        ax1f1.set_ylabel('Flujo térmico', color='b')
        
        cursor = FollowDotCursor(ax1f1, a, b, tolerance=20)
        
        return fig0, fig1
    
    def crearWidget(self, filtro, ep):
        fig10, fig11 = self.creaFiguras(filtro.tiempo, filtro.temp, filtro.flujo)
        canvas1 = FigureCanvas(fig10)
        canvas2 = FigureCanvas(fig11)
        vbox = QtGui.QGridLayout()
        vbox.addWidget(QtGui.QLabel("<b>Episodio:</b> " + filtro.tipo))
        vbox.addWidget(QtGui.QLabel("<b>Inicio:</b> " + str(filtro.tiempo[0])))
        vbox.addWidget(QtGui.QLabel("<b>Final:</b> " + str(filtro.tiempo[-1])))
        vbox.addWidget(QtGui.QLabel("<b>Duración:</b> %i min" % (len(filtro.tiempo))))
        vbox.addWidget(QtGui.QLabel("<b>Coeficiente de correlación:</b> " + str(filtro.correlacion)[:5]))
        vbox.addWidget(QtGui.QLabel("<b>Calorías consumidas:</b> " + str(filtro.numCalorias)[:6] + " (" + str(filtro.numCalorias/self.selep.totalCal*100)[:4] + "%)"))
        vbox.addWidget(canvas1)
        vbox.addWidget(canvas2)
        canvas2.mpl_connect('pick_event', lambda event: self.onpick(event, ep))
        return vbox
    
    #Inserta elementos en el layout con los nuevos episodios
    def updateView(self):
        if(len(self.selep.epFiltro) > 0):
            self.vbox = self.crearWidget(self.selep.epFiltro[self.epActual], 0)
            self.layoutMatplot1.addLayout(self.vbox)
            if(len(self.selep.epFiltro) > 1):
                self.vbox2 = self.crearWidget(self.selep.epFiltro[self.epActual+1], 1)
                self.layoutMatplot1.addLayout(self.vbox2)
                
    #Elimina el contenido del layout actual        
    def limpiarLayout(self):
        plt.close('all') #Cerrar todos las gráficas dibujadas para vaciar memoria   
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
        self.filSueno = self.cbSueno.isChecked() #Cambiar el filtro
        self.selep.update(self.filSueno, self.filSedentario, self.filLigero, self.filModerado) #Actualizar el array de episodios filtrados
        self.setBounds()
        self.limpiarLayout()
        #self.updateView()
        
    def filtrarSedentario(self):
        print "Filtrar sedentario"
        self.filSedentario = self.cbSedentario.isChecked()
        self.selep.update(self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.setBounds()
        self.limpiarLayout()
        #self.updateView()
        
    def filtrarLigera(self):
        print "Filtrar ligera"
        self.filLigero = self.cbLigera.isChecked()
        self.selep.update(self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.setBounds()
        self.limpiarLayout()
        #self.updateView()
        
    def filtrarModerada(self):
        print "Filtrar moderada"
        self.filModerado = self.cbModerada.isChecked()
        self.selep.update(self.filSueno, self.filSedentario, self.filLigero, self.filModerado)
        self.setBounds()
        self.limpiarLayout()
        #self.updateView()
    
    def retroceder(self):
        if (self.epActual > 0):
            self.epActual -= 1
            print "episodios", self.epActual, "y", self.epActual+1
            self.limpiarLayout()
            #self.updateView()
        
    def avanzar(self):
        if (self.epActual < len(self.selep.epFiltro) - 2):
            self.epActual += 1
            print "episodios", self.epActual, "y", self.epActual+1
            self.limpiarLayout()
            #self.updateView()
        
        
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    
    main.show()
    sys.exit(app.exec_())
    
    
