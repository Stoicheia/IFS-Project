# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""
from shapely.geometry import Polygon
from shapely.ops import unary_union
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
            s = sum([self.IFS[k-1].scaling for k in theta[0:i]])
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
        # print(f"k = {k} - attr:", self.attractor)
        if k == 0:
            return [Tile(a, []) for a in self.attractor] 
        addresses = self.omegaK(k)
        bigPolyVertices = self.attractor[0].exterior.coords
        # print(self.attractor.polygon)
        # print(self.theta)
        
        print(addresses)
        for sigma in addresses:
            projectionMatrix = np.eye(3)
            for i in sigma:
                projectionMatrix = np.matmul(projectionMatrix, self.IFS[i - 1].matrix)
            for j in self.theta[0:k]:
                projectionMatrix = np.matmul(self.IFS[j - 1].matrixInverse, projectionMatrix)
            vertices = []
            for vertex in bigPolyVertices:
                vertices.append(np.matmul(projectionMatrix, np.array([vertex[0], vertex[1], 1])))
            twoVertices = [(v[0], v[1]) for v in vertices]
            tilePoly = Polygon(twoVertices)
            tile = Tile(tilePoly, sigma)
            # print(tilePoly)
            # print(tile.address)
            otherPolys = unary_union([tile.polygon for tile in polygons])
            tile.subtract(otherPolys)
            if not tile.polygon.is_empty:
                polygons.append(tile)
        self.iterations[k] = polygons
        return polygons
    
    def omegaK(self, k):
        if k > 0:
            return self.omegaKPartial([], self.sumTheta[k])
        elif k == 0:
            return []
    
    def omegaKPartial(self, root, target):
        result = []
        rootSum = sum(self.IFS[k - 1].scaling for k in root)
        if(rootSum > target):
            return []
        for i in range(1, self.sigma + 1): # IFS = [f1, f2, f3] -> range(1, 4) = (1, 2, 3)
            rootPlusOne = root.copy()
            rootPlusOne.append(i)
            newSum = rootSum + self.IFS[i - 1].scaling
            if newSum >= target:
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
        [2, 0, 1],
        [0, 2, 1],
        [0, 0, 1]
        ])

    IFSNumber = 4;
    maxRand = 5;

    IFS = []
    for i in range(IFSNumber):
        IFS.append(
            IFSfunc(
                matrix = A, 
                scaling = 2
            )
        )

    # Attractors are the same
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    attractor = Tile(Polygon(points), [])

    # Generate Theta
    theta = [randint(0, IFSNumber-1) for i in IFS]
    print(theta)

    t = Tiling(IFS = IFS, attractor = attractor, theta = theta)
    print(t.getIteration(1))

