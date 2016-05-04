# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../lib')
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from sklearn import preprocessing
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import scipy.spatial.distance as ssd
import math
import mlpy
import cachitos


class HierarchicalClustering():
    def __init__(self, selepisodio, tf=False, cons=False):
        #Representa un episodio de sueño mediante las series temporales de flujo y temperatura
        class Individuo:
            def __init__(self, nombre, tiempo, temperatura=[], flujo=[], consumo=[]):
                self.nombre = nombre
                self.tiempo = tiempo
                self.stt = temperatura
                self.stf = flujo
                self.stc = consumo
        
        sel = selepisodio
        
        print "Normalizar", len(sel.epFiltro), "episodios de sueño"
        # Normalizar por estandarización cada episodio de sueño (temperatura y flujo)
        self.eps_sueno = []
        if(tf):
            for i in sel.epFiltro:
                a = preprocessing.scale(i.temp, copy=True)
                b = preprocessing.scale(i.flujo, copy=True)
                self.eps_sueno.append(Individuo(i.nombre, i.tiempo, temperatura=a, flujo=b))
        elif(cons):
            for i in sel.epFiltro:
                a = preprocessing.scale(i.consumo, copy=True)
                self.eps_sueno.append(Individuo(i.nombre, i.tiempo, consumo=a))
        """
        #La diagonal de distancias no da 0 con fastdtw, mismas ST dan distancias >0 !!!
        for i in range(s):
            print eps_sueno[i].stt[-1], eps_sueno[i].stt[-1]
        for i in range(s):
            d, p = fastdtw(eps_sueno[i].stt, eps_sueno[i].stt, dist=euclidean)
            dd, p = fastdtw(eps_sueno[i].stf, eps_sueno[i].stf, dist=euclidean)
            dt = mlpy.dtw_std(eps_sueno[i].stt, eps_sueno[i].stt, dist_only=True)
            df = mlpy.dtw_std(eps_sueno[i].stf, eps_sueno[i].stf, dist_only=True)
            print d, dd, dt, df
        """
        #Calcular matriz de distancias entre cada individuo por DTW
        s = len(self.eps_sueno)
        self.distancias = np.zeros((s, s))
        if(tf):
            for i in range(s):
                for j in range(s):
                    #distanceTemp , path = fastdtw(eps_sueno[i].stt, eps_sueno[j].stt, dist=euclidean) #Distancia en temperatura
                    #distanceFlujo , path = fastdtw(eps_sueno[i].stf, eps_sueno[j].stf, dist=euclidean) #Distancia en flujo
                    distanceTemp = mlpy.dtw_std(self.eps_sueno[i].stt, self.eps_sueno[j].stt, dist_only=True) #Dist. euclidea
                    distanceFlujo = mlpy.dtw_std(self.eps_sueno[i].stf, self.eps_sueno[j].stf, dist_only=True)
                    self.distancias[j][i] = math.sqrt(math.pow(distanceTemp, 2) + math.pow(distanceFlujo, 2)) #Distancia euclídea total
        elif(cons):
            for i in range(s):
                for j in range(s):
                    self.distancias[j][i] = mlpy.dtw_std(self.eps_sueno[i].stc, self.eps_sueno[j].stc, dist_only=True) #Dist. euclidea
        #Vector con las distancias requeridas para hacer clustering
        #print distancias
        print self.distancias.shape

        #Obtener la diagonal de la matriz de distancias
        dists = ssd.squareform(self.distancias)
        print dists
        #Calcular clustering jerárquico
        self.Z = linkage(dists, 'average')

        self.labels=[]
        for i in self.eps_sueno:
            self.labels.append(i.nombre)
        
    def getDendogram(self):
        #Dibujar dendograma
        f = plt.figure('Clustering')
        #plt.title('Dendograma de clustering jerarquico')
        plt.xlabel('Indice de episodio')
        plt.ylabel('Distancia')
        labels=[]
        for i in self.eps_sueno:
            labels.append(i.nombre)
        dendrogram(self.Z, leaf_rotation=20., leaf_font_size=8., labels = labels)
        #plt.show()
        return f
