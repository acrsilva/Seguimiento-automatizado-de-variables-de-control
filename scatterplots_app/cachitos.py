# -*- coding: utf-8 -*-

import numpy as np

csv = np.genfromtxt ('../data.csv', delimiter=",")
actSed = csv[:,18] #Sedentario
actLig = csv[:,19] #Ligera
actMod = csv[:,20] #Moderada
sueno = csv[:,25] #Sueño

class Episodio():
    def __init__(self, ini, fin, tipo):
        self.ini = ini
        self.fin = fin
        self.tipo = tipo

def cachitos(minep, maxct):
    indices = []
    a = False #Episodio empezado
    c = 0 #Indice de comienzo
    t = 0 #Contador de minutos de otra actividad
    f = 0 #Indice de final
    for i in range(len(sueno)):
        if(not a and sueno[i] != 0): #nuevo episodio
            c = i
            a = True
            f = i
        elif(a): #episodio comenzado
            if(sueno[i] != 0): #resetear tiempo otra actividad
                t = 0
                f = i
            elif(t < maxct): #otra actividad
                t = t + 1
            else: #fin del episodio
                if ((f-c) >= minep):
                    indices.append([c, f])
                t = 0
                a = False
                c = 0
                f = 0
    return indices

def cachitosT(minep, maxin):
    indices = []
    a = False #Episodio empezado
    t = 0 #Contador de minutos de otra actividad
    sed = False
    lig = False
    mod = False
    cs = 0
    cl = 0
    cm = 0
    for i in range(len(actSed)):
        if (actSed[i] and not a):
            sed = True
            a = True
            fs = i
            if (cs == 0):
                cs = i
        elif(sed and a):
            if(actSed[i]):
                t = 0
                fs = i
            elif(t<=maxin and actLig[i] or actMod[i]):
                t += 1
                if(t == 1 and actLig[i]):
                    cl = i
                elif(t == 1 and actMod[i]):
                    cm = i
            else:
                if (fs > cs and (fs-cs) >= minep):
                    indices.append([cs, fs])
                t = 0
                cs = 0
                a = False
                sed = False
        if(actLig[i] and not a):
            lig = True
            a = True
            fl = i
            if(cl == 0):
                cl = i
        elif(lig and a):
            if(actLig[i]):
                t = 0
                fl = i
            elif(t<=maxin and actSed[i] or actMod[i]):
                t += 1
                if(t == 1 and actSed[i]):
                    cs = i
                elif(t == 1 and actMod[i]):
                    cm = i
            else:
                if (fl > cl and fl-cl >= minep):
                    indices.append([cl, fl])
                t = 0
                cl = 0
                a = False
                lig = False
        if(actMod[i] and not a):
            mod = True
            a = True
            fm = i
            if(cm == 0):
                cm = i
        elif(mod and a):
            if(actMod[i]):
                t = 0
                f = i
            elif(t<=maxin and actSed[i] or actLig[i]):
                t += 1
                if(t == 1 and actLig[i]):
                    cl = i
                elif(t == 1 and actSed[i]):
                    cs = i
            else:
                if (fm > cm and (fm-cm) >= minep):
                    indices.append([cm, fm])
                t = 0
                cm = 0
                a = False
                mod = False
    return indices


trocitos = cachitosT(15, 9)
print  "Hay " + str(len(trocitos)) + " trocitos"
print trocitos


