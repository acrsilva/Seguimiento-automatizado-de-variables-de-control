# -*- coding: utf-8 -*-
import sys
#sys.path.insert(0, '../lib')
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from sklearn import preprocessing
from scipy.spatial.distance import euclidean
#from fastdtw import fastdtw
import scipy.spatial.distance as ssd
import math
import mlpy
import selEpisodio

DEBUG=0


class HierarchicalClustering():
    #episodios = selep
    def __init__(self, episodios, tf=False, cons=False):
        #Representa un episodio de sueño mediante las series temporales de flujo y temperatura
        class Individuo:
            def __init__(self, nombre, tiempo, temperatura=[], flujo=[], consumo=[]):
                self.nombre = nombre
                self.tiempo = tiempo
                self.stt = temperatura
                self.stf = flujo
                self.stc = consumo
        
        #episodios = selep.epFiltro
        
        print "Normalizar", len(episodios), "episodios de sueño"
        # Normalizar por estandarización cada episodio de sueño (temperatura y flujo)
        self.eps_sueno = []
        if(tf):
            for i in episodios:
                a = preprocessing.scale(i.temp, copy=True)
                b = preprocessing.scale(i.flujo, copy=True)
                self.eps_sueno.append(Individuo(i.nombre, i.tiempo, temperatura=a, flujo=b))
        elif(cons):
            for i in episodios:
                a = preprocessing.scale(i.consumo, copy=True)
                self.eps_sueno.append(Individuo(i.nombre, i.tiempo, consumo=a))
        
        #Calcular matriz de distancias entre cada individuo por DTW
        s = len(self.eps_sueno)
        self.distancias = np.zeros((s, s))
        if(tf):
            for i in range(s):
                for j in range(s):
                    #distanceTemp , path = fastdtw(eps_sueno[i].stt, eps_sueno[j].stt, dist=euclidean) #Distancia en temperatura
                    #distanceFlujo , path = fastdtw(eps_sueno[i].stf, eps_sueno[j].stf, dist=euclidean) #Distancia en flujo
                    distanceTemp = mlpy.dtw_std(self.eps_sueno[i].stt, self.eps_sueno[j].stt, dist_only=True) 
                    distanceFlujo = mlpy.dtw_std(self.eps_sueno[i].stf, self.eps_sueno[j].stf, dist_only=True)
                    self.distancias[j][i] = math.sqrt(math.pow(distanceTemp, 2) + math.pow(distanceFlujo, 2)) #Distancia euclídea total
        elif(cons):
            for i in range(s):
                for j in range(s):
                    self.distancias[j][i] = mlpy.dtw_std(self.eps_sueno[i].stc, self.eps_sueno[j].stc, dist_only=True) #Dist. euclidea
        #Vector con las distancias requeridas para hacer clustering
        if(DEBUG): print "Matriz de distancias", self.distancias.shape, self.distancias

        #Obtener la diagonal de la matriz de distancias
        dists = ssd.squareform(self.distancias)
        #Calcular clustering jerárquico
        self.Z = linkage(dists, 'average')

        self.labels=[]
        for i in self.eps_sueno:
            self.labels.append(i.nombre)
        
