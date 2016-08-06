# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
#sys.path.insert(0, '../lib')

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
from panelSueno import PanelSueno
from panelConsumo import PanelConsumo
from copy import copy
from panelInterprete import PanelInterprete

DEBUG = 0
PRUEBAS=0

Ui_MainWindow, QMainWindow = loadUiType('int_final.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        #self.showMaximized()
        #Cargar el diseño de la interfaz del QtDesigner
        self.setupUi(self)
        
        #self.__initGraphs__()
        self.loadData()
        
        #Conectar elementos de la interfaz
        self.actionAbrir.triggered.connect(self.abrirListener)
        self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.tabListener)
        
        print "Listo"
    
    def initTabs(self):
        self.tabs = []
        
        
        self.gvInterprete.clear()
        self.interprete = PanelInterprete(self.selep, self.csv, self.gvInterprete, self.btn_prev, self.btn_next, self.cbxEpisodio)
        self.tabs.append(self.interprete)
        sel1 = copy(self.selep)
        
        #Rellenar layouts
        self.tabs.append(PanelSueno(sel1, self.plotLayoutUp, self.plotLayoutBot, self.cbx1, self.cbx2, 
                            self.rbTemperatura, self.rbConsumo, self.lbl1, self.lbl2, self.tableLayout, self.dendrogramLayout))
        sel2 = copy(self.selep)
        sel2.update(sNocturno=False, sedentario=False, ligero=False, moderado=False)
        #self.selep.update(sNocturno=False, sedentario=False, ligero=False, moderado=False)
        if(len(sel2.epFiltro) > 0):
            self.tabs.append(PanelSueno(sel2, self.plotLayoutUpSiestas, self.plotLayoutBotSiestas, self.cbx1Siestas,
                                self.cbx2Siestas, self.rbTemperaturaSiestas, self.rbConsumoSiestas, self.lbl1Siestas,
                                self.lbl2Siestas, self.tableLayoutSiestas, self.dendrogramLayoutSiestas))
        else:
            self.tabWidget.setTabEnabled(2,False)
        #self.selep.update(sDiurno=False, sedentario=False, ligero=False, moderado=False)
        sel3 = copy(self.selep)
        sel3.update(sDiurno=False, sedentario=False, ligero=False, moderado=False)
        if(len(sel3.epFiltro) > 0):
            self.tabs.append(PanelSueno(sel3, self.plotLayoutUpSuenos, self.plotLayoutBotSuenos, self.cbx1Suenos,
                                self.cbx2Suenos, self.rbTemperaturaSuenos, self.rbConsumoSuenos, self.lbl1Suenos,
                                self.lbl2Suenos, self.tableLayoutSuenos, self.dendrogramLayoutSuenos))
        else:
            self.tabWidget.setTabEnabled(3,False)
            
        epsDias = []
        dd = self.csv.getDatosDias()
        for i in dd:
            epsDias.append(cachitos.selEpisodio(i))
        self.tabs.append(PanelConsumo(epsDias, self.layout_diario, self.layout_dia_izq, self.layout_dia_der,
                                  self.cbx_izq, self.cbx_der, self.lbl_izq, self.lbl_der))
        
        
    #Carga un fichero de datos csv y obtiene los episodios de sueño
    #Inicializa el contenido de la interfaz
    def loadData(self):
        if(PRUEBAS): fname = 'data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        self.csv = lf.LectorFichero(fname)
        self.selep = cachitos.selEpisodio(self.csv.getDatos(), sedentario=False, ligero=False, moderado=False)
        
        self.setWindowTitle('Estudio de sueños (' + fname +')')
        
        self.initTabs()
        
        
        #self.configureComboBox()
        #self.updatePlots('todos', ep1=True, ep2=True)
        #self.initCluster()
        #self.cluster()
        #self.setLabel(sup=True)
        #self.setLabel(sup=False)
        

    def tabListener(self):
        curTab = self.tabWidget.currentIndex()
        print "Tab ", curTab
        #self.tabs[curTab].loadData(self.
        
    def abrirListener(self):
        #Limpiar layouts
        self.tabWidget.setTabEnabled(2,True)
        self.tabWidget.setTabEnabled(3,True)
        
        self.interprete.clearGraphs()
        self.gvInterprete.clear()
        
        for i in reversed(range(self.layout_diario.count())): 
            self.layout_diario.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.layout_dia_izq.count())): 
            self.layout_dia_izq.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.layout_dia_der.count())): 
            self.layout_dia_der.itemAt(i).widget().deleteLater()    
        for i in reversed(range(self.tableLayout.count())): 
            self.tableLayout.itemAt(i).widget().deleteLater()    
        for i in reversed(range(self.plotLayoutUp.count())): 
            self.plotLayoutUp.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.plotLayoutBot.count())): 
            self.plotLayoutBot.itemAt(i).widget().deleteLater()       
        for i in reversed(range(self.dendrogramLayout.count())): 
            self.dendrogramLayout.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.plotLayoutUpSiestas.count())): 
            self.plotLayoutUpSiestas.itemAt(i).widget().deleteLater()       
        for i in reversed(range(self.plotLayoutBotSiestas.count())): 
            self.plotLayoutBotSiestas.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.tableLayoutSiestas.count())): 
            self.tableLayoutSiestas.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.dendrogramLayoutSiestas.count())): 
            self.dendrogramLayoutSiestas.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.plotLayoutUpSuenos.count())): 
            self.plotLayoutUpSuenos.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.plotLayoutBotSuenos.count())): 
            self.plotLayoutBotSuenos.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.plotLayoutUpSuenos.count())): 
            self.plotLayoutUpSuenos.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.tableLayoutSuenos.count())): 
            self.tableLayoutSuenos.itemAt(i).widget().deleteLater()   
        for i in reversed(range(self.dendrogramLayoutSuenos.count())): 
            self.dendrogramLayoutSuenos.itemAt(i).widget().deleteLater()   

        self.loadData()    



if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    
    sys.exit(app.exec_())
    
    
