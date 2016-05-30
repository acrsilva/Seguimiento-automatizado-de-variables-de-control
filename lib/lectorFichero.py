# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import codecs
import sys
from datetime import datetime as dt
from PyQt4 import QtGui

DEBUG = 0
PRUEBAS = 0

"""
Almacena los valores puros de un fichero csv
Puede separar los datos en días
"""
class Datos():
    def __init__(self, sueno, clasifSueno, flujo, temp, tiempo, actli, actsd, actmd, consm, acltrans):
        self.sueno = sueno
        self.clasifSueno = clasifSueno
        self.flujo = flujo
        self.temp = temp
        self.tiempo = tiempo #int
        self.actli = actli
        self.actsd = actsd
        self.actmd = actmd
        self.consm = consm
        self.acltrans = acltrans
    
    #Crea una lista días particionando los datos
    def creaDias(self):
        #Devuelve una lista con los datos de un día concreto
        def datosDia(dia):
            return Datos(self.sueno[dia[0]:dia[1]+1],
                        self.clasifSueno[dia[0]:dia[1]+1],
                        self.flujo[dia[0]:dia[1]+1],
                        self.temp[dia[0]:dia[1]+1],
                        self.tiempo[dia[0]:dia[1]+1],
                        self.actli[dia[0]:dia[1]+1],
                        self.actsd[dia[0]:dia[1]+1],
                        self.actmd[dia[0]:dia[1]+1],
                        self.consm[dia[0]:dia[1]+1],
                        self.acltrans[dia[0]:dia[1]+1])
        
        datos_dias = []
        ini, fin = 0, 0
        for i in range(len(self.tiempo)-1):
            fecha1 = dt.fromtimestamp(self.tiempo[i])
            fecha2 = dt.fromtimestamp(self.tiempo[i+1])
            #Nuevo dia si cambia el dia o si es el último
            if(fecha1.day != fecha2.day or i == len(self.tiempo)-2):
                fin = i
                datos_dias.append(datosDia((ini, fin)))
                if(DEBUG):
                    print "ini", dt.fromtimestamp(self.tiempo[ini]), "fin", dt.fromtimestamp(self.tiempo[fin])
                
                ini = i+1
                
        return datos_dias
        
            
"""
Obtiene los datos de un fichero csv y crea los episodios
"""
class LectorFichero(object):
    """
    Inicializa la matriz con los valores del csv
    
    Parametros de entrada
    - nombre: nombre del fichero csv que contiene los datos
    - dias: además de todos los datos, obtener los de cada día separados en 24h de 00 a 00
    
    Atributos:
    - datos_total: una estructura Datos que contiene todos los datos originales del fichero csv
    - datos_dias: una estructura Datos por cada día natural
    """
    def __init__(self, nombre):
        csv = np.genfromtxt(open(nombre, 'r'), delimiter="," , names=True)
        #self.nomCols = self.csv.dtype.names
        #self.nparams = len(self.nomCols)

        sueno = csv['Sueño'.encode('iso8859-15')]
        clasifSueno = csv['Clasificaciones_del_sueño'.encode('iso8859-15')]
        flujo = csv['Flujo_térmico__media'.encode('iso8859-15')]
        temp = csv['Temp_cerca_del_cuerpo__media']
        tiempo = csv['Time'] / 1000
        actli = csv['Ligera']
        actsd = csv['Sedentaria']
        actmd = csv['Moderada']
        consm = csv['Gasto_energético'.encode('iso8859-15')]
        acltrans = csv['Acel_transversal__picos']
        
        #Datos tal cual vienen en el csv, sin particiones
        self.datos_total = Datos(sueno, clasifSueno, flujo, temp, tiempo, actli, actsd, actmd, consm, acltrans)
        
    def getDatos(self):
        return self.datos_total
        
    def getDatosDias(self):
        datos_dias = self.datos_total.creaDias()
        if(DEBUG):
            print len(self.datos_dias), 'dias'
            for i in self.datos_dias:
                print "ini", i.tiempo[0], "fin", i.tiempo[-1]
        return datos_dias

if(PRUEBAS):
    fichero = LectorFichero('../data.csv')
    fichero.getDatosDias()
    #raw_input('Press <ENTER> to continue')
    
    """
    datos.datosPorDia(datos.dias[2], 'sueno')
    print len(datos.datosPorDia(datos.dias[6], 'sueno'))
    for i in datos.dias:
        dia = datos.datosPorDia(i, 'tiempo')
        print dt.utcfromtimestamp(dia[0])
        print dt.utcfromtimestamp(dia[len(dia)-1])
    """
               

