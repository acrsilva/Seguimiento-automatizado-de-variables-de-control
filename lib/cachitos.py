# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
from datetime import datetime
from scipy.stats import pearsonr
import leeFichero
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

#Definición de tipos
tipoSueno = "sueño"
tipoSedentario = "sedentario"
tipoLigera = "ligero"
tipoModerado = "moderado"

#Estructura con la información de un episodio
class Episodio():
    def __init__(self, ini, fin, tipo, nombre):
        self.ini = ini
        self.fin = fin
        self.tipo = tipo
        self.nombre = nombre
    def filtrar(self, tiempo, temperaturas, flujo, consumo):
        self.tiempo = tiempo[self.ini:self.fin]
        self.temp = temperaturas[self.ini:self.fin]
        self.flujo = flujo[self.ini:self.fin]
        self.correlacion, p = pearsonr(self.temp, self.flujo)
        self.numCalorias = sum(consumo[self.ini:self.fin])
    

class selEpisodio():
    def __init__(self, filename, sueno=True, sedentario=True, ligero=True, moderado=True):
        self.csv = leeFichero.LeeFichero(open(filename, 'r'))
        
        #Pasar minutos a Datetime
        self.dt = [] 
        for i in self.csv.tiempo:
            self.dt.append(datetime.fromtimestamp(i))
        
        ind = self.cachitos2(15, 4, self.csv.sueno, self.csv.actsd, self.csv.actli, self.csv.actmd)
        self.episodios = self.creaEpisodios2(5, 35, 7, 4, 3, ind)
        
        self.epFiltro = []
        self.update(sueno, sedentario, ligero, moderado)
        self.totalCal = sum(self.csv.consm)
        
    #Crea el array de episodios con los filtros aplicados
    def update(self, sueno=True, sedentario=True, ligero=True, moderado=True):
        #print self.filSueno, self.filSedentario, self.filLigero, self.filModerado, len(self.epFiltro)
        print sueno, sedentario, ligero, moderado, len(self.epFiltro)
        self.epFiltro = []
        for i in self.episodios:
            if((i.tipo == tipoSueno and sueno) 
                or (i.tipo == tipoSedentario and sedentario)
                or (i.tipo == tipoLigera and ligero)
                or (i.tipo == tipoModerado and moderado)):
                self.epFiltro.append(i)
                self.epFiltro[-1].filtrar(self.dt, self.csv.temp, self.csv.flujo, self.csv.consm)
        print "Total episodios:", len(self.episodios) 
        print "Total eps con filtros:", len(self.epFiltro)

    def comprobar(self, ls1, ls2, ls3, i, c1, c2, c3, f, t, maxin, final):
        """
        Comprueba si la interrupcion ha llegado al maximo permitido
        con lo que activa final para cambiar de episodio o activa los
        instantes de inicio de los otros tipos de episodio cuando
        detecta el inicio de una interrupción
        """
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
        
    def cachitoSueno(self):
        """
        Busca los índices de inicio y final de los episodios de sueño
        """
        indices = []
        a = False #Episodio empezado
        c = 0 #Indice de comienzo
        t = 0 #Contador de minutos despierto
        f = 0 #Indice de final
        for i in range(len(self.csv.sueno)):
            if(not a and self.csv.sueno[i] != 0): #nuevo episodio
                c = i
                a = True
                f = i
            elif(a): #episodio comenzado
                if(self.csv.sueno[i] != 0): #dormido(resetear tiempo despierto)
                    t = 0
                    f = i
                elif(t < 60): #despierto(cuanto tiempo?)
                    t = t + 1
                else: #fin del episodio (1h seguida despierto)
                    if ((f-c)>10):
                        indices.append(Episodio(c, f, tipoSueno, ""))
                    t = 0
                    a = False
        return indices

    #minep: intervalo mínimo por episodio en minutos
    #maxin: intervalo máximo para considerar interrupción
    def cachitos(self, minep, maxin):
        """
        Crea los distintos episodios teniendo en cuenta el maximo intervalo
        de interrupcion y el tamaño minimo de un episodio.
        Devuelve una lista con los indices de inicio y final de cada episodio
        además del tipo de episodio
        """
        indices = []
        a = False #Episodio empezado
        t = 0 #Contador de minutos de otra actividad
        sed, lig, mod, final = False, False, False, False
        cs, cl, cm = 0, 0, 0
        fs, fl, fm = 0, 0, 0
        for i in range(len(self.csv.actsd)):
            if (self.csv.actsd[i] == 1 and not a):
                a, sed = True, True            
                fs = i
                t = 0
                if (cs == 0):
                    cs = i
            elif(sed and a):
                fs, cl, cm, t, final = self.comprobar(self.csv.actsd, self.csv.actli, self.csv.actmd, i, cs, cl, cm, fs, t, maxin, final)
                if (final):
                    if (fs > cs and (fs-cs) >= minep):
                        #indices.append([cs,fs])
                        indices.append(Episodio(cs, fs, tipoSedentario, ""))
                    t, cs = 0, 0
                    a, final, sed = False, False, False
            if(self.csv.actli[i] == 1 and not a):
                a, lig = True, True
                t = 0
                fl = i
                if(cl == 0):
                    cl = i
            elif(lig and a):
                fl, cs, cm, t, final = self.comprobar(self.csv.actli, self.csv.actsd, self.csv.actmd, i, cl, cs, cm, fl, t, maxin, final)
                if (final):
                    if (fl > cl and (fl-cl) >= minep):
                        #indices.append([cs,fs])
                        indices.append(Episodio(cl, fl, tipoLigera, ""))
                    t, cl = 0, 0
                    a, final, lig = False, False, False
            if(self.csv.actmd[i] == 1 and not a):
                a, mod = True, True
                t = 0
                fm = i
                if(cm == 0):
                    cm = i
            elif(mod and a):
                fm, cs, cl, t, final = self.comprobar(self.csv.actmd, self.csv.actsd, self.csv.actli, i, cm, cs, cl, fm, t, maxin, final)
                if (final):
                    if (fm > cm and (fm-cm) >= minep):
                        #indices.append([cs,fs])
                        indices.append(Episodio(cm, fm, tipoModerado, ""))
                    t, cm = 0, 0
                    a, final, mod = False, False, False
        return indices

    #minep: intervalo mínimo por episodio en minutos
    #maxin: intervalo máximo para considerar interrupción
    def creaEpisodios(self, minep, maxin):
        """
        Con los episodios de sueño y los distintos tipos de actividad física
        se crean los episodios finales. Para ello se cortan los episodios de
        actividad que contengan a los de sueño.
        """
        s = self.cachitoSueno()
        actividad = self.cachitos(minep, maxin)
        eps = []
        j = 0
        for a in actividad:
            if(s[j].ini < a.fin and s[j].ini > a.ini and s[j].fin < a.fin):
                if (s[j].ini-1 - a.ini >= minep):
                    eps.append(Episodio(a.ini, s[j].ini-1, a.tipo, ""))
                eps.append(Episodio(s[j].ini, s[j].fin, s[j].tipo, ""))
                if (a.fin - s[j].fin+1 >= minep):
                    eps.append(Episodio(s[j].fin+1, a.fin, a.tipo, ""))
                if(j < len(s)-1):
                    j += 1
            else:
                eps.append(a)
        return eps
        
    def cumpleMin(self, minep, lista):
        cumple = False
        i = 0
        while i < len(lista) and not cumple:
            if(lista[i].fin - lista[i].ini > minep):
                cumple = True
            i += 1
        return cumple
        
    def actualizaEp(self, i, op, lista):
        """
        Elimina episodios de la lista que interrumpen a otro episodio
        incluyéndolos dentro del que interrumpen
        """
        if(op == 2):
            nuevoEp = Episodio(lista[i].ini, lista[i+2].fin, lista[i].tipo, "")
            lista.remove(lista[i+2])
            lista.remove(lista[i+1])
            lista[i] = nuevoEp
        elif(op == 3):
            nuevoEp = Episodio(lista[i].ini, lista[i+3].fin, lista[i].tipo, "")
            lista.remove(lista[i+3])
            lista.remove(lista[i+2])
            lista.remove(lista[i+1])
            lista[i] = nuevoEp
        return lista
    
    def cortaMinep(self, minep, lista):
        """
        Borra los episodios que no cumplan con el minimo de tamaño
        """
        i = 0
        nums = [0, 0, 0, 0]
        while i < len(lista):
            if lista[i].fin - lista[i].ini + 1 < minep:
                lista.remove(lista[i])
            elif lista[i].tipo == tipoSedentario and lista[i].fin - lista[i].ini + 1 < 7:
                lista.remove(lista[i])
            else:
                i += 1
        i = 0
        while i < len(lista)-1:
            if lista[i].tipo == lista[i+1].tipo:
                lista[i] = Episodio(lista[i].ini, lista[i+1].fin, lista[i].tipo, "")
                lista.remove(lista[i+1])
            self.ponerNombres(lista[i], nums)
            i += 1
        self.ponerNombres(lista[i], nums)
        return lista
        
    def ponerNombres(self, episodio, nums):
        """
        Pone nombres a los episodios según su tipo y además los enumera
        """
        if episodio.tipo == tipoSueno:
            nums[0] += 1
            episodio.nombre = str(nums[0]) + ". Sueño"
        elif episodio.tipo == tipoSedentario:
            nums[1]  += 1
            episodio.nombre = str(nums[1]) + ". Sedentario"
        elif episodio.tipo == tipoLigera:
            nums[2] += 1
            episodio.nombre = str(nums[2]) + ". Ligera"
        elif episodio.tipo == tipoModerado:
            nums[3] += 1
            episodio.nombre = str(nums[3]) + ". Moderada"
        
    def creaEpisodios2(self, minep, mxsni, mxsdi, mxlgi, mxmdi, lista):
        """
        Crea episodios de las distintas actividades con interrupciones variables
        para cada uno dependiendo de su importancia
        mxsni: maxima interrupcion en un episodio de sueño
        mxsdi: maxima interrupcion en un episodio de actv sedentaria
        mslgi: maxima interrupcion en un episodio de actv ligera
        mxmdi: maxima interrupcion en un episodio de actv moderada
        """
        i = 0
        while self.cumpleMin(minep, lista) and i < len(lista)-3:
            if lista[i].fin - lista[i].ini + 1:
                if lista[i].tipo == lista[i+2].tipo :
                    if(lista[i].tipo == tipoModerado and lista[i+1].fin - lista[i+1].ini < mxmdi):
                        lista = self.actualizaEp(i, 2, lista)
                    elif(lista[i].tipo == tipoSueno and lista[i+1].fin - lista[i+1].ini < mxsni):
                        lista = self.actualizaEp(i, 2, lista)
                    elif(lista[i].tipo == tipoLigera and lista[i+1].fin - lista[i+1].ini < mxlgi):
                        lista = self.actualizaEp(i, 2, lista)
                    elif(lista[i].tipo == tipoSedentario and lista[i+1].fin - lista[i+1].ini < mxsdi):
                        lista = self.actualizaEp(i, 2, lista)
                    else:
                        i += 1
                elif lista[i].tipo == lista[i+3].tipo :
                    uno = lista[i+1].fin - lista[i+1].ini + 1
                    dos = lista[i+2].fin - lista[i+2].ini + 1
                    if(lista[i].tipo == tipoSueno and uno + dos < mxsni):
                        lista = self.actualizaEp(i, 3, lista)
                    elif(lista[i].tipo == tipoSedentario and uno + dos < mxsdi):
                        lista = self.actualizaEp(i, 3, lista)
                    elif(lista[i].tipo == tipoLigera and uno + dos < mxlgi):
                        lista = self.actualizaEp(i, 3, lista)
                    elif(lista[i].tipo == tipoModerado and uno + dos < mxmdi):
                        lista = self.actualizaEp(i, 3, lista)
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        self.cortaMinep(minep, lista)
        return lista
        
    
    def encuentraTipo(self, indice, sueno, sed, lig, mod):
        """
        Devuelve el tipo de actividad que se realiza y activa
        el flag de ese tipo
        """
        if(sueno[indice] == 1):
            return tipoSueno, True, False, False, False
        elif(sueno[indice] == 0):
            if(sed[indice] == 1):
                return tipoSedentario, False, True, False, False
            elif(lig[indice] == 1):
                return tipoLigera, False, False, True, False
            elif(mod[indice] == 1):
                return tipoModerado, False, False, False, True

    def cachitos2(self, minep, maxin, sueno, sed, lig, mod):
        """
        Crea los distintos episodios teniendo en cuenta el maximo intervalo
        de interrupcion.
        Devuelve una lista con los indices de inicio y final de cada episodio
        además del tipo de episodio y nombre
        """
        indices = []
        cini, cfin = 0, 0
        tipo, sbool, sedb, ligb, modb = self.encuentraTipo(0, sueno, sed, lig, mod)
        for i in range(len(sueno)-1):
            if(sueno[i+1] == 1 and not sbool):
                cfin = i
                indices.append(Episodio(cini, cfin, tipo, ""))
                tipo, sbool, sedb, ligb, modb = self.encuentraTipo(i+1, sueno, sed, lig, mod)
                cini = i+1
            elif(sueno[i+1] == 0):
                if(sed[i+1] == 1 and not sedb):
                    cfin = i
                    indices.append(Episodio(cini, cfin, tipo, ""))
                    tipo, sbool, sedb, ligb, modb = self.encuentraTipo(i+1, sueno, sed, lig, mod)
                    cini = i+1
                elif(lig[i+1] == 1 and not ligb):
                    cfin = i
                    indices.append(Episodio(cini, cfin, tipo, ""))
                    tipo, sbool, sedb, ligb, modb = self.encuentraTipo(i+1, sueno, sed, lig, mod)
                    cini = i+1
                elif(mod[i+1] == 1 and not modb):
                    cfin = i
                    indices.append(Episodio(cini, cfin, tipo, ""))
                    tipo, sbool, sedb, ligb, modb = self.encuentraTipo(i+1, sueno, sed, lig, mod)
                    cini = i+1
        indices.append(Episodio(cini, len(sueno)-1, tipo, ""))
        return indices
        

eps = selEpisodio('../data.csv')
ind = eps.cachitos2(15, 4, eps.csv.sueno, eps.csv.actsd, eps.csv.actli, eps.csv.actmd)
print len(ind)
for i in range(1):
    print ind[i].ini, ind[i].fin, ind[i].tipo

print len(ind)
print "Agrupados"
nind = eps.creaEpisodios2(5, 35, 7, 4, 3, ind)
for i in range(len(nind)):
    print nind[i].nombre, "duracion:", nind[i].fin - nind[i].ini + 1
print len(nind)


vs = 0
for i in range(len(ind)):
    if (ind[i].tipo == tipoSueno):
        vs += 1
        print ind[i].nombre, ind[i].ini, ind[i].fin, "duracion:", ind[i].fin - ind[i].ini+1
print vs
