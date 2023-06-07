# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:53:40 2023

@author: pieis
"""

from shapely.geometry import Polygon
import numpy as np
from numpy.linalg import inv
from shapely.errors import GEOSException 

class Tile:
    
    def __init__(self, polygon, address):
        self.polygon = polygon
        self.address = address
        
    def subtract(self, otherPoly):
        try:
            newPoly = self.polygon.difference(otherPoly)
            self.__init__(newPoly, self.address)
        except GEOSException: # Sometimes it will raise a TopologyException when computing differences between two lines
            pass


class IFSfunc:
    def __init__(self, scaling, matrix, edge = [0,0]):
        self.scaling = scaling
        self.matrix = matrix
        self.edge = edge
        self.matrixInverse = inv(matrix)
    
    def apply(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrix, vec)
        return (newVec[0], newVec[1])
    
    def applyInverse(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrixInverse, vec)
        return (newVec[0], newVec[1])
    
class graphVertex:
    def __init__(self, polygon):
        self.polygon = polygon
        self.outgoing = []
        self.ingoing = []
        
    def addEdgeOutgoing(self, edgeIndex):
        self.outgoing.append(edgeIndex)
            
    def addEdgeIngoing(self, edgeIndex):
        self.ingoing.append(edgeIndex)

class graphEdge:
    def __init__(self, fromIndex, toIndex, func):
        self.fromIndex = fromIndex
        self.toIndex = toIndex
        self.func = func
        
class IFSgraph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        for i in range(len(self.edges)):
            edge = self.edges[i]
            self.vertices[edge.fromIndex].addEdgeOutgoing(i)
            self.vertices[edge.fromIndex].addEdgeIngoing(i)
        self.sigma = len(edges)
        print(vertices)
        print(edges)

        
    def getAdjacentEdges(self, vertexIndex):
        return self.vertices[vertexIndex].outgoing
    
    def getFunc(self, index):
        return self.edges[index].func
    
    def getPoly(self, vIndex):
        return self.vertices[vIndex].polygon
            
    # gives list of all valid addresses
    def omegaK(self, k, theta):
        thetaSum = sum([self.getFunc(j).scaling for j in theta[0:k]])
        allPaths = []
        if k > 0:
            allPaths += self.omegaKPartial([], thetaSum, self.edges[theta[-1]].toIndex)
            return allPaths
        elif k == 0:
            return []
    
    def omegaKPartial(self, root, target, vIndex):
        result = []
        rootSum = sum(self.getFunc(k).scaling for k in root)
        if(rootSum > target):
            return []
        for i in self.vertices[vIndex].ingoing: # IFS = [f1, f2, f3] -> range(1, 4) = (1, 2, 3)
            rootPlusOne = root.copy()
            rootPlusOne.append(i)
            newSum = rootSum + self.getFunc(i).scaling
            if newSum >= target:
                result += [rootPlusOne]
            else:
                result += self.omegaKPartial(rootPlusOne, target, self.edges[i].fromIndex)
        return result
        