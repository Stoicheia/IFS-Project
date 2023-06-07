# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:06:42 2023

@author: pieis
"""

from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from IFSLibrary import Tile

class graphEdge:
    def __init__(self, fromIndex, toIndex, func):
        self.fromIndex = fromIndex
        self.toIndex = toIndex
        self.func = func
        
            

        


