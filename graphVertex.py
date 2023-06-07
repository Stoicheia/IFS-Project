# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:03:50 2023

@author: pieis
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:02:48 2023

@author: pieis
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:42:56 2023

@author: pieis
"""
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from IFSLibrary import Tile

class graphVertex:
    def __init__(self, polygon):
        self.polygon = polygon
        self.outgoing = []
        self.ingoing = []
        
    def addEdgeOutgoing(self, edgeIndex):
        self.outgoing.append(edgeIndex)
            
    def addEdgeIngoing(self, edgeIndex):
        self.ingoing.append(edgeIndex)

        


