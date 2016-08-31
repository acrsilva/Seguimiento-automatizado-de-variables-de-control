# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
#sys.path.insert(0, '../lib')

from PyQt4.uic import loadUiType
from pyqtgraph.Qt import QtCore, QtGui
import lectorFichero as lf
import selEpisodio
from panelSueno import PanelSueno
from panelConsumo import PanelConsumo
from panelScatter import PanelScatter
from copy import copy
from panelInterprete import PanelInterprete

DEBUG = 0

Ui_MainWindow, QMainWindow = loadUiType('int_final.ui')


class VentanaMain(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(VentanaMain, self).__init__()
        #self.showMaximized()
        
        #Cargar el diseño de la interfaz del QtDesigner
        self.setupUi(self)
        
        self.init = 0
        #self.loadData()
        
        #Conectar elementos de la interfaz
        self.actionAbrir.triggered.connect(self.abrirListener)
        print "Listo"
    
    def initTabs(self):
        """ Inicializa cada pestaña de la ventana principal """
        self.tabs = []
        
        #Pestaña interprete (0)
        self.gvInterprete.clear()
        self.interprete = PanelInterprete(self.selep, self.csv, self.gvInterprete, self.btn_prev, self.btn_next, self.cbxEpisodio)
        self.tabs.append(self.interprete)
        
        #Pestaña scatterplots (1)
        sel4 = copy(self.selep)
        sel4.update(sDiurno=True, sNocturno=True, sedentario=True, ligero=True, moderado=True)
        self.scatter = PanelScatter(sel4, self.layoutMatplot1, self.cbSueno, self.cbSedentario, self.cbLigera, self.cbModerada, 
                                    self.cbx_izq_2, self.cbx_der_2, self.btnPrev, self.btnNext, self.labelScatter)
        self.tabs.append(self.scatter)
        
        #Pestaña sueños (todos) (2)
        sel1 = copy(self.selep)
        self.tabs.append(PanelSueno(self, sel1, self.plotLayoutUp, self.plotLayoutBot, self.cbx1, self.cbx2, self.rbTemperatura, 
                                    self.rbConsumo, self.lbl1, self.lbl2, self.tableLayout, self.dendrogramLayout, self.btnFiltraEpsT))
        
        #Pestaña sueños diurnos (3)
        sel2 = copy(self.selep)
        sel2.update(sNocturno=False, sedentario=False, ligero=False, moderado=False)
        if(len(sel2.epFiltro) > 0):
            self.tabs.append(PanelSueno(self, sel2, self.plotLayoutUpSiestas, self.plotLayoutBotSiestas, self.cbx1Siestas,
                                self.cbx2Siestas, self.rbTemperaturaSiestas, self.rbConsumoSiestas, self.lbl1Siestas,
                                self.lbl2Siestas, self.tableLayoutSiestas, self.dendrogramLayoutSiestas, self.btnFiltraEpsD))
        else:
            self.tabWidget.setTabEnabled(3,False)
        
        #Pestaña sueños nocturnos (4)    
        sel3 = copy(self.selep)
        sel3.update(sDiurno=False, sedentario=False, ligero=False, moderado=False)
        if(len(sel3.epFiltro) > 0):
            self.tabs.append(PanelSueno(self, sel3, self.plotLayoutUpSuenos, self.plotLayoutBotSuenos, self.cbx1Suenos,
                                self.cbx2Suenos, self.rbTemperaturaSuenos, self.rbConsumoSuenos, self.lbl1Suenos,
                                self.lbl2Suenos, self.tableLayoutSuenos, self.dendrogramLayoutSuenos, self.btnFiltraEpsN))
        else:
            self.tabWidget.setTabEnabled(4,False)
        
        #Pestaña consumos (5)    
        epsDias = []
        dd = self.csv.getDatosDias()
        for i in dd:
            epsDias.append(selEpisodio.selEpisodio(i))
        self.tabs.append(PanelConsumo(epsDias, self.layout_diario, self.layout_dia_izq, self.layout_dia_der,
                                  self.cbx_izq, self.cbx_der, self.lbl_izq, self.lbl_der))
        
        
    #Carga un fichero de datos csv y obtiene los episodios de sueño
    #Inicializa el contenido de la interfaz
    def loadData(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        
        self.init = 1
        
        print "Abriendo fichero ", fname
        self.csv = lf.LectorFichero(fname) #self.csv.getDatos()
        self.selep = selEpisodio.selEpisodio(self.csv.getDatos(), sedentario=False, ligero=False, moderado=False)
        self.setWindowTitle('Estudio de sueños (' + fname +')')
        
        self.clearData()
        
        self.initTabs()
        

    def clearData(self):
        try:
            #Limpiar layouts
            self.tabWidget.setTabEnabled(2,True)
            self.tabWidget.setTabEnabled(3,True)
            
            self.interprete.clearGraphs()
            self.gvInterprete.clear()
            
            self.scatter.limpiarLayout()
                    
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
        except:
            print ""
            
    def abrirListener(self):
        self.loadData()    



if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    main = VentanaMain()
    
    main.show()
    
    sys.exit(app.exec_())
    
    
