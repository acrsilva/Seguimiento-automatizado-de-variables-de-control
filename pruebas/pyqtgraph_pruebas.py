import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from pylab import *
import matplotlib.pyplot as plt
import numpy as np

csv = np.genfromtxt ('../data.csv', delimiter=",")
t = csv[:,0] / 1000 #Tiempo

temperaturas = csv[:,8] #Temperatura
a = int(t[0])
b = int(t[-1])
print a,b, (b-a)/60

tt = []
temp = []

k = 0
for i in range(a, b+60, 60):
    if(t[k] == i):
        tt.append(t[k])
        temp.append(temperaturas[k])
        k +=1
    else:
        tt.append(np.nan)
        temp.append(np.nan)
    
    
win = pg.GraphicsWindow()
win.resize(800,350)
plt1 = win.addPlot()
plt1.plot(tt, temp, connect='finite')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
