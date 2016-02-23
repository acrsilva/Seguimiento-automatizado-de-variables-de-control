# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intbarras.ui'
#
# Created: Tue Feb 23 20:28:14 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

"""

Prueba para insertar la prueba de gráfico de barras con episodio de sueño
utilizando Qt designer
Código de interfaz compilado mediante el comando:
	pyuic4 -x intbarras.ui -o pruebainterfazbar.py
	
"""


from PyQt4 import QtCore, QtGui
import numpy as np
import pyqtgraph as pg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(480, 481)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 360, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 360, 98, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(100, 60, 256, 192))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))

from pyqtgraph import GraphicsView

#Cargar los datos
csv = np.genfromtxt ('data.csv', delimiter=",")
x = csv[:,1]
y = csv[:,25]

#Trocear datos en episodios
a = -1
b = -1
c = 0
for i in range(len(y)):
	if(y[i] != 0 and a == -1): #dormido
		a = i #comienzo del episodio
	elif(y[i] == 0 and a != -1 and b < 100): #despierto
		b = b + 1
	elif(b >= 100 and c == 0):
		c = 1
		b = i #fin del episodio
	k = i
print "a:%i b:%i k:%i\n" %(a, b, k)

#Elegir episodio a mostrar
n = b-a
x = x[a:b]
y = y[a:b]
xGrid = np.linspace(x[0], x[-1], n)
yGrid = np.interp(xGrid, x, y)

colors = []
num = 0
for i in y:
	if(i == 2): #Sueño ligero - Naranja
		c = pg.mkColor(255, 128, 0)
	elif(i == 4): #Sueño profundo - Amarillo
		c = pg.mkColor(255, 255, 0)
	elif(i == 5): #Sueño muy profundo - Verde
		c = pg.mkColor(0, 255, 0)
		#print "Verde! en %i\n" % num
	else: #Despierto - Rojo
		c = pg.mkColor(255, 0, 0)
	colors.append(c)
	num = num + 1

barGraphItem = pg.BarGraphItem()
barGraphItem.setOpts(x0=xGrid[:-1], x1=xGrid[1:], y0=[0] * n, height=0.3, brushes=colors, pens=colors)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    plt = pg.PlotItem()
    plt.getViewBox().setMouseEnabled(True, False)

    ui.graphicsView.setCentralItem(plt)
    plt.addItem(barGraphItem)
    
    MainWindow.show()
    sys.exit(app.exec_())

