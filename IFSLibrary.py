# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:53:40 2023

@author: pieis
"""

from shapely.geometry import Polygon
import numpy as np
from numpy.linalg import inv

class Tile(Polygon):
    def __init__(self, points, address):
        self.address = address
        super().__init__(points)
        
    def subtract(self, other):
        self.__init__(self.difference(other).exterior.coords.xy, self.address)


class IFSfunc:
    def __init__(self, scaling, matrix):
        self.scaling = scaling
        self.matrix = matrix
        self.matrixInverse = inv(matrix)
    
    def apply(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrix, vec)
        return (newVec[0], newVec[1])
    
    def applyInverse(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrixInverse, vec)
        return (newVec[0], newVec[1])