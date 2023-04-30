# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""

class Tiling:
    def __init__(self, IFS, attractor, theta):
        self.IFS = IFS
        self.attractor = attractor
        self.theta = theta
        self.thetaLength = len(theta)
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
    
    