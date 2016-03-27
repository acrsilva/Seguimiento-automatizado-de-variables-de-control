# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import datetime


csv = np.genfromtxt ('../data.csv', delimiter=",")
t = csv[:,0] / 1000 #Tiempo
actSed = csv[:,18] #Sedentario
actLig = csv[:,19] #Ligera
actMod = csv[:,20] #Moderada
sueno = csv[:,25] #Sueño

temperaturas = csv[:,8] #Temperatura
flujos = csv[:,26] #Flujo

dt = []

for i in t:
    dt.append(datetime.datetime.fromtimestamp(i))

#Definición de tipos
tipoSueno = "sueño"
tipoSedentario = "sedentario"
tipoLigera = "ligera"
tipoModerado = "moderado"

#Estructura con la información de un episodio
class Episodio():
    def __init__(self, ini, fin, tipo):
        self.ini = ini
        self.fin = fin
        self.tipo = tipo
    def filtrar(self):
        self.tiempo = dt[self.ini:self.fin]
        self.temp = temperaturas[self.ini:self.fin]
        self.flujo = flujos[self.ini:self.fin]
        
        
def comprobar(ls1, ls2, ls3, i, c1, c2, c3, f, t, maxin, final):
    if(ls1[i] == 1):
        t = 0
        f = i
    elif(t <= maxin):
        t += 1
        if(t == 1 and ls2[i] == 1):
            c2 = i
            c3 = 0
        elif(t == 1 and ls3[i] == 1):
            c3 = i
            c2 = 0
    else:
        final = True
    return f, c2, c3, t, final
    
def cachitoSueno():
    indices = []
    a = False #Episodio empezado
    c = 0 #Indice de comienzo
    t = 0 #Contador de minutos despierto
    f = 0 #Indice de final
    for i in range(len(sueno)):
        if(not a and sueno[i] != 0): #nuevo episodio
            c = i
            a = True
            f = i
        elif(a): #episodio comenzado
            if(sueno[i] != 0): #dormido(resetear tiempo despierto)
                t = 0
                f = i
            elif(t < 60): #despierto(cuanto tiempo?)
                t = t + 1
            else: #fin del episodio (1h seguida despierto)
                if ((f-c)>10):
                    indices.append(Episodio(c, f, tipoSueno))
                t = 0
                a = False
    return indices

#minep: intervalo mínimo por episodio en minutos
#maxin: intervalo máximo para considerar interrupción
def cachitos(minep, maxin):
    indices = []
    a = False #Episodio empezado
    t = 0 #Contador de minutos de otra actividad
    sed, lig, mod, final = False, False, False, False
    cs, cl, cm = 0, 0, 0
    fs, fl, fm = 0, 0, 0
    for i in range(len(actSed)):
        if (actSed[i] == 1 and not a):
            a, sed = True, True            
            fs = i
            t = 0
            if (cs == 0):
                cs = i
        elif(sed and a):
            fs, cl, cm, t, final = comprobar(actSed, actLig, actMod, i, cs, cl, cm, fs, t, maxin, final)
            if (final):
                if (fs > cs and (fs-cs) >= minep):
                    #indices.append([cs,fs])
                    indices.append(Episodio(cs, fs, tipoSedentario))
                t, cs = 0, 0
                a, final, sed = False, False, False
        if(actLig[i] == 1 and not a):
            a, lig = True, True
            t = 0
            fl = i
            if(cl == 0):
                cl = i
        elif(lig and a):
            fl, cs, cm, t, final = comprobar(actLig, actSed, actMod, i, cl, cs, cm, fl, t, maxin, final)
            if (final):
                if (fl > cl and (fl-cl) >= minep):
                    #indices.append([cs,fs])
                    indices.append(Episodio(cl, fl, tipoLigera))
                t, cl = 0, 0
                a, final, lig = False, False, False
        if(actMod[i] == 1 and not a):
            a, mod = True, True
            t = 0
            fm = i
            if(cm == 0):
                cm = i
        elif(mod and a):
            fm, cs, cl, t, final = comprobar(actMod, actSed, actLig, i, cm, cs, cl, fm, t, maxin, final)
            if (final):
                if (fm > cm and (fm-cm) >= minep):
                    #indices.append([cs,fs])
                    indices.append(Episodio(cm, fm, tipoModerado))
                t, cm = 0, 0
                a, final, mod = False, False, False
    return indices

#minep: intervalo mínimo por episodio en minutos
#maxin: intervalo máximo para considerar interrupción
def creaEpisodios(minep, maxin):
    s = cachitoSueno()
    actividad = cachitos(minep, maxin)
    eps = []
    j = 0
    for a in actividad:
        if(s[j].ini < a.fin and s[j].ini > a.ini and s[j].fin < a.fin):
            if (s[j].ini-1 - a.ini >= minep):
                eps.append(Episodio(a.ini, s[j].ini-1, a.tipo))
            eps.append(Episodio(s[j].ini, s[j].fin, s[j].tipo))
            if (a.fin - s[j].fin+1 >= minep):
                eps.append(Episodio(s[j].fin+1, a.fin, a.tipo))
            if(j < len(s)-1):
                j += 1
        else:
            eps.append(a)
    return eps

class selEpisodio():
    def __init__(self):
        self.episodios = creaEpisodios(15,9)
        self.filSueno = True
        self.filSedentario = True
        self.filLigero = True
        self.filModerado = True
        self.epFiltro = []
        self.update()
        
    #Crea el array de episodios con los filtros aplicados
    def update(self):
        print self.filSueno, self.filSedentario, self.filLigero, self.filModerado, len(self.epFiltro)
        self.epFiltro = []
        for i in self.episodios:
            if((i.tipo == tipoSueno and self.filSueno) 
                or (i.tipo == tipoSedentario and self.filSedentario)
                or (i.tipo == tipoLigera and self.filLigero)
                or (i.tipo == tipoModerado and self.filModerado)):
                self.epFiltro.append(i)
                self.epFiltro[-1].filtrar()
        
        
#pruba = selEpisodio()


"""
trocitos =  cachitos(15,6)
s, l, m = 0, 0, 0
#print trocitos

for i in trocitos:
    if (i.tipo == tipoSedentario):
        s += 1
        print i.ini, i.fin, i.tipo
    elif(i.tipo == tipoLigera):
        l += 1
        print i.ini, i.fin, i.tipo
    elif(i.tipo == tipoModerado):
        m += 1
        print i.ini, i.fin, i.tipo
print str(s) + "S " + str(l) + "L " + str(m) + "M "
print len(trocitos)
"""
"""
suenete = cachitoSueno()
for i in suenete:
    print i.ini, i.fin, i.tipo

epis = creaEpisodios(15, 9)
for i in epis:
    print i.ini, i.fin, i.tipo
print len(epis)
"""
