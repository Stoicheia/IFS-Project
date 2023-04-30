# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""

import numpy as np
from IFSLibrary import Tile

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
        for i in range(len(self.iterations), k + 1):
            self.iterations.append([])
        if self.iterations[k] == []:
            return self.calculateIteration(k)
        else:
            return self.iterations[k]
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
            for vertex in bigPolyVertices:
                vertices.append(np.matmul(projectionMatrix, vertex))
            tilePoly = Tile(vertices, sigma)
            for existingPolygon in polygons:
                tilePoly.subtract(existingPolygon)
            polygons.append(tilePoly)
        self.iterations[k] = polygons
        return polygons
            
            
    
    def omegaK(self, k):
        return self.omegaKPartial([], self.sumTheta[k])
    
    def omegaKPartial(self, root, target):
        result = []
        rootSum = sum(self.IFS[k].scaling for k in root)
        if(rootSum > target):
            return []
        for i in range(self.sigma):
            rootPlusOne = root.copy()
            rootPlusOne.append(i)
            newSum = rootSum + self.IFS[i].scaling
            if newSum > target:
                result += [rootPlusOne]
            else:
                result += self.omegaKPartial(rootPlusOne, target)
        return result
    
    
    
    

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
                scaling = randint(1, maxRand)
            )
        )

    # Attractors are the same
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    attractors = [Polygon(points)]

    # Generate Theta
    theta = [randint(0, IFSNumber-1) for i in IFS]
    print(theta)

    t = Tiling(IFS = IFS, attractor = attractors, theta = theta)
    print(t.omegaK(1))

