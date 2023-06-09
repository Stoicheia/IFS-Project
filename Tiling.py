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
    def __init__(self, IFSgraph, theta):
        # IFS a list of [IFSfunc]. IFSfunc has scaling, apply and applyinv
        self.IFSgraph = IFSgraph

        # List of integers
        self.theta = theta

        self.thetaLength = len(theta)

        # List of theta sums
        self.sumTheta = []
        self.iterations = []
        for i in range(len(theta)):
            s = sum([self.IFSgraph.edges[k-1].func.scaling for k in theta[0:i]])
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
        if k == 0:
            return [Tile(self.IFSgraph.vertices[self.IFSgraph.edges[self.theta[0]].fromIndex].polygon, [])] 
        addresses = self.IFSgraph.omegaK(k, self.theta)
        
        for sigma in addresses:
            initialPoly = self.IFSgraph.getPoly(self.IFSgraph.edges[sigma[-1]].toIndex)
            bigPolyVertices = initialPoly.exterior.coords
            projectionMatrix = np.eye(3)
            s = sigma.copy()
            s.reverse()
            for i in sigma:
                projectionMatrix = np.matmul(projectionMatrix, self.IFSgraph.edges[i].func.matrix)
            thetak = self.theta[0:k]
            thetak
            for j in thetak:
                projectionMatrix = np.matmul(self.IFSgraph.edges[j].func.matrixInverse, projectionMatrix)
            vertices = []
            for vertex in bigPolyVertices:
                vertices.append(np.matmul(projectionMatrix, np.array([vertex[0], vertex[1], 1])))
            twoVertices = [(v[0], v[1]) for v in vertices]
            tilePoly = Polygon(twoVertices)
            tile = Tile(tilePoly, sigma)

            polygons.append(tile)
        self.iterations[k] = polygons
        return polygons

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

   # t = Tiling(IFSgraph = IFSgraph, theta = theta)
    #print(t.getIteration(1))

