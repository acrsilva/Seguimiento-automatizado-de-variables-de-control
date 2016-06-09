# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../lib')

from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
import lectorFichero as lf
import colores
import clustering
import cachitos
from panelSueno import PanelSueno
from tablaDistancias import TablaDistancias


DEBUG = 0
PRUEBAS=1



Ui_MainWindow, QMainWindow = loadUiType('int_estudio_sueno_nuevo.ui')
        

# plotLayout
# cbx1, cbx2
# btnAbrir, btnClustering
# rbTemperatura, rbConsumo
# tableDistancias
# dendrogramLayout
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        #self.showMaximized()
        #Cargar el diseño de la interfaz del QtDesigner
        self.setupUi(self)
        
        #self.__initGraphs__()
        self.loadData()
        
        #Conectar elementos de la interfaz
        self.actionAbrir.triggered.connect(self.loadData)
        self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.tabListener)
        
        print "Listo"
    
    def initTabs(self):
        self.tabs = []
        self.tabs.append(PanelSueno(self.selep, self.plotLayoutUp, self.plotLayoutBot, self.cbx1, self.cbx2, 
                            self.rbTemperatura, self.rbConsumo, self.lbl1, self.lbl2, self.tableLayout, self.dendrogramLayout))
        
        
        self.selep.update(sNocturno=False, sedentario=False, ligero=False, moderado=False)
        self.tabs.append(PanelSueno(self.selep, self.plotLayoutUpSiestas, self.plotLayoutBotSiestas, self.cbx1Siestas,
                            self.cbx2Siestas, self.rbTemperaturaSiestas, self.rbConsumoSiestas, self.lbl1Siestas,
                            self.lbl2Siestas, self.tableLayoutSiestas, self.dendrogramLayoutSiestas))
        
        self.selep.update(sDiurno=False, sedentario=False, ligero=False, moderado=False)
        self.tabs.append(PanelSueno(self.selep, self.plotLayoutUpSuenos, self.plotLayoutBotSuenos, self.cbx1Suenos,
                            self.cbx2Suenos, self.rbTemperaturaSuenos, self.rbConsumoSuenos, self.lbl1Suenos,
                            self.lbl2Suenos, self.tableLayoutSuenos, self.dendrogramLayoutSuenos))
        
    #Carga un fichero de datos csv y obtiene los episodios de sueño
    #Inicializa el contenido de la interfaz
    def loadData(self):
        if(PRUEBAS): fname = '../data.csv'
        else: fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        print "Abriendo fichero ", fname
        csv = lf.LectorFichero(fname).getDatos()
        self.selep = cachitos.selEpisodio(csv, sedentario=False, ligero=False, moderado=False)
        
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
        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    
    main.show()
    
    sys.exit(app.exec_())
    
    
