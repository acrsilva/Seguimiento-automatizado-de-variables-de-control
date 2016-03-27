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
                    indices.append(Episodio(cs, fs, "Sedentario"))
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
                    indices.append(Episodio(cl, fl, "Ligera"))
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
                    indices.append(Episodio(cm, fm, "Moderada"))
                t, cm = 0, 0
                a, final, mod = False, False, False
    return indices

"""
trocitos =  cachitos(15,6)
s, l, m = 0, 0, 0
#print trocitos

for i in trocitos:
    
    if (i.tipo == "Sedentario"):
        s += 1
        print i.ini, i.fin, i.tipo
    elif(i.tipo == "Ligera"):
        l += 1
        print i.ini, i.fin, i.tipo
    elif(i.tipo == "Moderada"):
        m += 1
        print i.ini, i.fin, i.tipo
print str(s) + "S " + str(l) + "L " + str(m) + "M "
print len(trocitos)
"""
