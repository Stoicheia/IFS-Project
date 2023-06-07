# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:02:48 2023

@author: pieis
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from IFSLibrary import Tile

class IFSgraph:
    
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        for i in range(len(self.edges)):
            edge = self.edges[i]
            self.vertices[edge.fromIndex].addEdgeOutgoing(i)
            self.vertices[edge.fromIndex].addEdgeIngoing(i)
        self.sigma = len(edges)

        
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
            allPaths.append(self.omegaKPartial([], thetaSum, self.edges[theta[-1]].toIndex))
            return allPaths
        elif k == 0:
            return []
    
    def omegaKPartial(self, root, target, vIndex):
        result = []
        rootSum = sum(self.getFunc(k - 1).scaling for k in root)
        if(rootSum > target):
            return []
        for i in self.vertices[vIndex].ingoing: # IFS = [f1, f2, f3] -> range(1, 4) = (1, 2, 3)
            rootPlusOne = root.copy()
            rootPlusOne.append(i)
            newSum = rootSum + self.getFunc(i - 1).scaling
            if newSum >= target:
                result += [rootPlusOne]
            else:
                result += self.omegaKPartial(rootPlusOne, target, self.edges[i - 1].fromIndex)
        return result
        
    
    
    
    

       
            
        


