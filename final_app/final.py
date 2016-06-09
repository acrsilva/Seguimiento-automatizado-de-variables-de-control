# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../lib')

import matplotlib.pyplot as plt
from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import matplotlib.dates as md
import math
import lectorFichero as lf
import colores
import clustering
from scipy.cluster.hierarchy import dendrogram
from datetime import datetime
import cachitos

DEBUG = 0
PRUEBAS=1

Ui_MainWindow, QMainWindow = loadUiType('int_final.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        #Cargar el diseño de la interfaz del QtDesigner
        self.setupUi(self)





if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    
    sys.exit(app.exec_())
    
    