"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import os
import time
import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

pg.mkQApp()

path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'interfaz_episodios.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        
        #scSueno = self.ui.wScatterSueno
        
        self.canvas
        
        self.show()
        
    def addmpl(self, fig):
        self.canvas.setParent(self.mplwindow)
        self.ui.wScatterSueno.add(self.canvas)
        self.canvas.draw()    
        

fig1 = Figure()
ax1f1 = fig1.add_subplot(111)
ax1f1.plot(np.random.rand(5))  
        
mwin = MainWindow()      
mwin.addmpl(fig1)  

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

"""


from PyQt4.uic import loadUiType
 
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
    
Ui_MainWindow, QMainWindow = loadUiType('interfaz_episodios.ui')



class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)
        
    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.layoutMatplot.addWidget(self.canvas)
        self.canvas.draw()
 
if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
 
    fig1 = Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(np.random.rand(5))
 
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
    
    
