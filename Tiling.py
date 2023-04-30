# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""

class Tiling:
    def __init__(self, IFS, attractor, theta):
        # IFS a list of [IFSfunc]. IFSfunc has scaling, apply and applyinv
        self.IFS = IFS

        # List of polygons
        self.attractor = attractor

        # List of integers
        self.theta = theta

        self.thetaLength = len(theta)

        # List of theta sums
        self.sumTheta = []
        self.iterations = []
        for i in range(len(theta)):
            self.sumTheta.append(sum(theta[0:i+1]))
            
    def getIteration(self, k):
        # if iteration stored, read, else calculateIteration(k)
        pass
            
    def calculateIteration(self, k):
        pass
    
    def omegaK(self, k):
        # lexicographically ordered indices 
        pass
    
    