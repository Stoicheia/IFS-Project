# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:06:04 2023

@author: pieis
"""

import numpy as np
from numpy.linalg import inv

class IFSfunc:
    def __init__(self, s, m):
        self.scaling = s
        self.matrix = m
        self.matrixInverse = inv(m)
    
    def apply(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrix, vec)
        return (newVec[0], newVec[1])
    
    def applyInverse(self, x, y):
        vec = np.array([x,y,1])
        newVec = np.matmul(self.matrixInverse, vec)
        return (newVec[0], newVec[1])