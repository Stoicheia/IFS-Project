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
            self.sumTheta.append(sum([IFS[i].scaling for i in theta[0:i+1]]))
            
    def getIteration(self, k):
        # if iteration stored, read, else calculateIteration(k)
        pass
            
    def calculateIteration(self, k):
        pass
    
    def omegaK(self, k):
        # lexicographically ordered indices 
        pass
    
    

if __name__ == "__main__":
    from IFSLibrary import IFSfunc
    import numpy as np
    from random import randint
    from shapely.geometry import Polygon

    # Generate IFS
    A = np.array([ # IFS matrix is fixed
        [1, 1, 1],
        [0, 2, 3],
        [0, 0, 1]
        ])

    IFSNumber = 10;
    maxRand = 5;

    IFS = []
    for i in range(IFSNumber):
        IFS.append(
            IFSfunc(
                matrix = A, 
                scaling = randint(1, maxRand + 1)
            )
        )

    # Attractors are the same
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    attractors = [Polygon(points)]

    # Generate Theta
    theta = [randint(0, IFSNumber) for i in IFS]
    print(theta)

    t = Tiling(IFS = IFS, attractor = attractors, theta = theta)


