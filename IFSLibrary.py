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