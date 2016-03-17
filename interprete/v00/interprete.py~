# -*- encoding: utf-8 -*-

from PyQt4 import QtGui
import pyqtgraph as pg
import numpy as np

# Inicializar GUI
app = QtGui.QApplication([])

# Inicializar ventana principal
mw = QtGui.QMainWindow()
mw.setWindowTitle(('Intérprete de sueños').decode("utf8"))
mw.resize(800,600)

# Definir el widget donde guardaremos todos los elementos
w = QtGui.QWidget()

# Añadir el widget contenedor a la ventana principal
mw.setCentralWidget(w)

# Crear otros widgets
plotDia = pg.PlotWidget(name='PlotDia')
plotEpi = pg.PlotWidget(name='PlotEpisodio')
btnPrevDia = QtGui.QPushButton(('Día anterior').decode("utf8"))
btnSigDia = QtGui.QPushButton(('Día siguiente').decode("utf8"))

# Configurar las gráficas
plotDia.setLabel('left', 'Tipo de sueño', units='');
plotDia.setLabel('bottom', 'Instante', units='minutos');
plotEpi.setLabel('left', 'Tipo de sueño', units='');
plotEpi.setLabel('bottom', 'Instante', units='minutos');

# Organizar los widgets mediante un grid
layout = QtGui.QGridLayout()
w.setLayout(layout)

# Añadir los widgets al layout
layout.addWidget(plotDia, 0, 0);
layout.addWidget(plotEpi, 1, 0);
layout.addWidget(btnPrevDia);
layout.addWidget(btnSigDia);

# Datos de ejemplo a mostrar
#x2 = np.linspace(-100, 100, 1000)
#data2 = np.sin(x2) / x2

# Datos desde csv a mostrar
csv = np.genfromtxt ('data.csv', delimiter=",")
tiempo = csv[:,0]
sueno = csv[:,25]


# Contenido de la gráfica superior (día)
curve = plotDia.plot(sueno, clickable=False)
#curve.curve.setClickable(True)
curve.setPen('w')  ## white pen
#curve.setShadowPen(pg.mkPen((70,70,30), width=6, cosmetic=True))

def clicked():
    print("curve clicked")
curve.sigClicked.connect(clicked)

# Definir la amplitud inicial de la lupa y sus límites
lr = pg.LinearRegionItem([0, 1000], bounds=[0,len(tiempo)], movable=True)
plotDia.addItem(lr)
#line = pg.InfiniteLine(angle=90, movable=True)
#plotDia.addItem(line)
#line.setBounds([0,200])

# Contenido de la gráfica inferior (episodio ~ zoom del día)
plotEpi.plot(sueno)
def updatePlot():
    plotEpi.setXRange(*lr.getRegion(), padding=0)
def updateRegion():
    lr.setRegion(plotEpi.getViewBox().viewRange()[0])
lr.sigRegionChanged.connect(updatePlot)
plotEpi.sigXRangeChanged.connect(updateRegion)
updatePlot()


mw.show()

app.exec_()
