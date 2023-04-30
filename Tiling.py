# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""

import numpy as np

class Tiling:
    def __init__(self, IFS, attractor, theta):
        # IFS a list of [IFSfunc]. IFSfunc has scaling, apply and applyinv
        self.IFS = IFS

        # List of polygons
        self.attractor = attractor

        # List of integers
        self.theta = theta

        self.thetaLength = len(theta)
        self.sigma = len(IFS)

        # List of theta sums
        self.sumTheta = []
        self.iterations = []
        for i in range(len(theta)):
            s = sum([self.IFS[k].scaling for k in theta[0:i]])
            self.sumTheta.append(s)
            
    def getIteration(self, k):
        # if iteration stored, read, else calculateIteration(k)
        pass
            
    def calculateIteration(self, k):
        polygons = []
        addresses = self.omegaK(k)
        bigPolyVertices = self.attractor.exterior.coords.xy
        for sigma in addresses:
            projectionMatrix = np.eye(3)
            for i in sigma:
                projectionMatrix = np.matmul(projectionMatrix, self.IFS[i].matrix)
            for j in self.theta[0:k]:
                projectionMatrix = np.matmul(self.IFS[j].matrixInverse, projectionMatrix)
            vertices = []
            
            
    
    def omegaK(self, k):
        return self.omegaKPartial([], self.sumTheta[k])
    
    def omegaKPartial(self, root, target):
        result = []
        rootSum = sum(self.IFS[k].scaling for k in root)
        for i in range(self.sigma):
            rootPlusOne = root
            rootPlusOne.append(i)
            newSum = rootSum + self.IFS[i].scaling
            if newSum > target:
                result += [rootPlusOne]
            else:
                result += self.omegaKPartial(rootPlusOne, target)
        return result
    
    
    
    