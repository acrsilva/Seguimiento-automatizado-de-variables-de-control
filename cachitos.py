# -*- coding: utf-8 -*-

import numpy as np

csv = np.genfromtxt ('data.csv', delimiter=",")
actSed = csv[:,18] #Sedentario
actLig = csv[:,19] #Ligera
actMod = csv[:,20] #Moderada
sueno = csv[:,25] #Sueño

def cachitos(lista, minep, maxct):
    indices = []
    a = False #Episodio empezado
    c = 0 #Indice de comienzo
    t = 0 #Contador de minutos de otra actividad
    f = 0 #Indice de final
    for i in range(len(lista)):
        if(not a and lista[i] != 0): #nuevo episodio
            c = i
            a = True
            f = i
        elif(a): #episodio comenzado
            if(lista[i] != 0): #resetear tiempo otra actividad
                t = 0
                f = i
            elif(t < maxct): #otra activiidad
                t = t + 1
            else: #fin del episodio
                if ((f-c) >= minep):
                    indices.append([c, f])
                t = 0
                a = False
                c = 0
                f = 0
    return indices

def cachitosT():
    indices = []
    a = False #Episodio empezado
    c = 0 #Indice de comienzo
    t = 0 #Contador de minutos de otra actividad
    f = 0 #Indice de final
    i = 0 
    """for i in range(len(actLig)):
        if(not a and (actSed[i] or actLig[i] or actMod[i])): #nuevo episodio
            c = i
            a = True
            f = i
        elif(a): #episodio comenzado
            if(actSed[i]): #resetear tiempo otra actividad
                t = 0
                f = i
            elif(t < 5): #otra activiidad
                t = t + 1
            else: #fin del episodio
                if ((f-c) >= 15):
                    indices.append([c, f])
                t = 0
                a = False
                c = 0
                f = 0
    return indices"""
    while (i < range(len(actSed))):
		if(not a and (actSed[i] or actLig[i] or actMod[i])): #nuevo episodio
			c = i
			a = True
			f = i
		elif(a):
			if

"""trocitos = cachitos(actSed, 15, 5)
print  "Hay " + str(len(trocitos)) + " trozos sedentarios"
trocitos = cachitos(actLig, 15, 5)
print  "Hay " + str(len(trocitos)) + " trozos ligeros"
trocitos = cachitos(actMod, 15, 5)
print  "Hay " + str(len(trocitos)) + " trozos moderados"
trocitos = cachitos(sueno, 10, 60)
print  "Hay " + str(len(trocitos)) + " trozos de sueño"

print cachitos(actSed, 15, 10)
print cachitos(actLig, 15, 10)
print cachitos(actMod, 15, 10)
print cachitos(sueno, 10, 60)
"""
trocitos = cachitosT()
print  "Hay " + str(len(trocitos)) + " trozos"
