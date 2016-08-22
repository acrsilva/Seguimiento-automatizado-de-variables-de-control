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
            #if(fecha1.day != fecha2.day or i == len(self.tiempo)-2):
            if((fecha1.day != fecha2.day and fecha1 < fecha2) or i == len(self.tiempo)-2):
                fin = i
                datos_dias.append(datosDia((ini, fin)))
                if(DEBUG == 1):
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
        self.nombre = nombre
        
        self.sueno = csv['Sueño'.encode('iso8859-15')]
        self.clasifSueno = csv['Clasificaciones_del_sueño'.encode('iso8859-15')]
        self.flujo = csv['Flujo_térmico__media'.encode('iso8859-15')]
        self.temp = csv['Temp_cerca_del_cuerpo__media']
        self.tiempo = csv['Time'] / 1000
        self.actli = csv['Ligera']
        self.actsd = csv['Sedentaria']
        self.actmd = csv['Moderada']
        self.consm = csv['Gasto_energético'.encode('iso8859-15')]
        self.acltrans = csv['Acel_transversal__picos']
        
        #COMPROBAR DATOS CORRECTOS
        self.filtrarDatosLigero()
        #self.comprobarDatos()
        #self.limpia_datos()
        
        #Datos tal cual vienen en el csv, sin particiones
        self.datos_total = Datos(self.sueno, self.clasifSueno, self.flujo, self.temp, self.tiempo, self.actli, self.actsd, self.actmd, self.consm, self.acltrans)
    
    def filtrarDatosLigero(self):
        def appendValues():
            sueno.append(self.sueno[i])
            clasifSueno.append(self.clasifSueno[i])
            flujo.append(self.flujo[i])
            temp.append(self.temp[i])
            actli.append(self.actli[i])
            actsd.append(self.actsd[i])
            actmd.append(self.actmd[i])
            consm.append(self.consm[i])
            acltrans.append(self.acltrans[i])
            
        numDatos = len(self.tiempo)
        i=10
        incorrectos = 0
        
        while(self.tiempo[i] % 60 != 0):
            i += 1
        t = self.tiempo[i]
        tiempo, sueno, clasifSueno, flujo, temp, actli, actsd, actmd, consm, acltrans = [], [], [], [], [], [], [], [], [], []

        if(DEBUG == 3):
            print i, self.tiempo[i], t
            raw_input() # PAUSE
            print "----Comprobar datos ", self.nombre, "----"
            print self.tiempo[i], t
            raw_input() # PAUSE
        
        """
        x = i
        while(x < 10):
            print self.tiempo[x+1] - self.tiempo[x]
            x += 1
        raw_input() # PAUSE    
        """
        
        while(i < numDatos-1):
            if(self.tiempo[i] % 60 != 0):
                if(DEBUG == 3):
                    print i
                    raw_input() # PAUSE
                    incorrectos += 1
                #tiempo.append(t)
                #appendNan()
            else:
                tiempo.append(t)
                appendValues()
                t += 60
            i += 1
               
        if(DEBUG == 3):
            print "Datos totales: ", numDatos, " incorrectos: ", incorrectos, " datos nuevos: ", len(tiempo)
        self.sueno, self.clasifSueno, self.flujo, self.temp, self.tiempo, self.actli, self.actsd, self.actmd, self.consm, self.acltrans = sueno, clasifSueno, flujo, temp, tiempo, actli, actsd, actmd, consm, acltrans    
    
    
    def comprobarDatos(self):
        def appendNan():
            sueno.append(np.NaN)
            clasifSueno.append(np.NaN)
            flujo.append(np.NaN)
            temp.append(np.NaN)
            actli.append(np.NaN)
            actsd.append(np.NaN)
            actmd.append(np.NaN)
            consm.append(np.NaN)
            acltrans.append(np.NaN)
        def appendValues():
            sueno.append(self.sueno[i])
            clasifSueno.append(self.clasifSueno[i])
            flujo.append(self.flujo[i])
            temp.append(self.temp[i])
            actli.append(self.actli[i])
            actsd.append(self.actsd[i])
            actmd.append(self.actmd[i])
            consm.append(self.consm[i])
            acltrans.append(self.acltrans[i])
               
        numDatos = len(self.tiempo)
        i=10
        incorrectos = 0
        
        while(self.tiempo[i] % 60 != 0):
            i += 1
        t = self.tiempo[i]
        tiempo, sueno, clasifSueno, flujo, temp, actli, actsd, actmd, consm, acltrans = [], [], [], [], [], [], [], [], [], []

        if(DEBUG == 3):
            print i, self.tiempo[i], t
            raw_input() # PAUSE
            print "----Comprobar datos ", self.nombre, "----"
            print self.tiempo[i], t
            raw_input() # PAUSE
        
        """
        x = i
        while(x < 10):
            print self.tiempo[x+1] - self.tiempo[x]
            x += 1
        raw_input() # PAUSE    
        """
        
        while(i < numDatos-1):
            if(self.tiempo[i] % 60 != 0):
                if(DEBUG == 3):
                    print i
                    raw_input() # PAUSE
                    incorrectos += 1
                #tiempo.append(t)
                #appendNan()
            elif(self.tiempo[i] != t):
                if(DEBUG == 3):
                    print "Desajuste de tiempo en ", i, " ", t, " ", self.tiempo[i]
                    raw_input() # PAUSE
                    incorrectos +=1
                if(self.tiempo[i] > t):
                    k = 0
                    #Si hay un salto de tiempo, rellenar el hueco con NaN
                    while(self.tiempo[i] > t):
                        #print i, self.tiempo[i], t
                        tiempo.append(t)
                        appendNan()
                        t+=60
                        k+=1
                    if(DEBUG == 3):
                        print "nan insertados: ", k
                        raw_input() # PAUSE
                tiempo.append(t)
                appendValues()
                t+=60
            else:
                tiempo.append(t)
                appendValues()
                t += 60
            i += 1
               
        if(DEBUG == 3):
            print "Datos totales: ", numDatos, " incorrectos: ", incorrectos, " datos nuevos: ", len(tiempo)
        self.sueno, self.clasifSueno, self.flujo, self.temp, self.tiempo, self.actli, self.actsd, self.actmd, self.consm, self.acltrans = sueno, clasifSueno, flujo, temp, tiempo, actli, actsd, actmd, consm, acltrans    
    
    def limpia_datos(self):
        print "Limpiando datos del fichero"
        i = 1
        dato = self.tiempo[0]
        numDatos = len(self.tiempo)
        # ¿? Mejor duplicar listas guardando en la segunda los datos filtrados
        while  (i < numDatos-1):
            if (self.tiempo[i] < self.tiempo[i-1] or (self.tiempo[i] - 90000) > self.tiempo[i-1]):
                numDatos -= 1
                print "*****Pillado!***** ", self.tiempo[i]
                np.delete(self.sueno, i)
                np.delete(self.clasifSueno, i)
                np.delete(self.flujo, i)
                np.delete(self.temp, i)
                np.delete(self.tiempo, i)
                np.delete(self.actli, i)
                np.delete(self.actsd, i)
                np.delete(self.actmd, i)
                np.delete(self.consm, i)
                np.delete(self.acltrans, i)
                
                
            else:    
                i += 1

    def getDatos(self):
        return self.datos_total
        
    def getDatosDias(self):
        datos_dias = self.datos_total.creaDias()
        if(DEBUG == 2):
            print len(datos_dias), 'dias'
            for i in datos_dias:
                print "ini", i.tiempo[0], "fin", i.tiempo[-1]
        return datos_dias



if(PRUEBAS):
    fname = 'Ejemplos/natividad.csv'
    fname2 = 'Ejemplos/Concha Muñoz Gutiérrez.csv'
    fname3 = 'Ejemplos/Ana Carolina.csv'
    fname4 = 'Ejemplos/noelia.csv'
    fname5 = 'Ejemplos/Javier.csv'
    
    fichero = LectorFichero(fname)
    #fichero = LectorFichero(fname2)
    #fichero = LectorFichero(fname3)
    #fichero = LectorFichero(fname4)
    #fichero = LectorFichero(fname5)

    #fichero.getDatosDias()
    #raw_input('Press <ENTER> to continue')
    
    """
    datos.datosPorDia(datos.dias[2], 'sueno')
    print len(datos.datosPorDia(datos.dias[6], 'sueno'))
    for i in datos.dias:
        dia = datos.datosPorDia(i, 'tiempo')
        print dt.utcfromtimestamp(dia[0])
        print dt.utcfromtimestamp(dia[len(dia)-1])
    """
               

