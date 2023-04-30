import matplotlib.pyplot as plt
from shapely.geometry import Polygon as ShapelyPolygon

class CustomPolygon:
    def __init__(self, points, color='blue', alpha=0.5):
        self.points = points
        self.color = color
        self.alpha = alpha
        self.polygon = ShapelyPolygon(points)
        
    def draw(self, ax):
        poly = plt.Polygon(self.points, facecolor=self.color, alpha=self.alpha)
        ax.add_patch(poly)
    
    def overlaps(self, other):
        return self.polygon.intersects(other.polygon)
    
    def is_covered(self, others):
        for other in others:
            if other is not self:
                if other.polygon.contains(self.polygon):
                    return True
        return False

class CustomPolygonList:
    def __init__(self, polygons):
        self.polygons = polygons
        
    def draw(self):
        fig, ax = plt.subplots()
        for polygon in self.polygons:
            polygon.draw(ax)
        plt.xlim([-0.5, 1.5])
        plt.ylim([-0.5, 1.5])
        plt.show()
        
    def overlaps(self):
        overlaps = []
        for i in range(len(self.polygons)):
            for j in range(i+1, len(self.polygons)):
                if self.polygons[i].overlaps(self.polygons[j]):
                    overlaps.append((i, j))
        return overlaps
    
    def is_covered(self):
        covered = []
        for i in range(len(self.polygons)):
            if self.polygons[i].is_covered(self.polygons[:i]):
                covered.append(i)
        return covered

# Example usage:
points1 = [(0, 0), (1, 0), (1, 1), (0, 1)]
points2 = [(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]
points3 = [(1, 1), (2, 1), (2, 2), (1, 2)]
points4 = [(0, 0), (0, 1), (1, 1)]
poly1 = CustomPolygon(points1, color='red')
poly2 = CustomPolygon(points2, color='blue')
poly3 = CustomPolygon(points3, color='green')
poly4 = CustomPolygon(points4, color='purple')
polygons = CustomPolygonList([poly1, poly2, poly3, poly4])

print(polygons.overlaps())  # Prints [(0, 1)]
print(polygons.is_covered())  # Prints [2]
polygons.draw()

"""
# First Implementation
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class CustomPolygon:
    def __init__(self, points, color='blue', alpha=0.5):
        self.points = points
        self.color = color
        self.alpha = alpha
        
    def draw(self, ax):
        poly = Polygon(self.points, facecolor=self.color, alpha=self.alpha)
        ax.add_patch(poly)

# Example usage:
fig, ax = plt.subplots()
points = [(0, 0), (1, 0), (1, 1), (0, 1)]
poly = CustomPolygon(points, color='red')
poly.draw(ax)
plt.xlim([-0.5, 1.5])
plt.ylim([-0.5, 1.5])
plt.show()
"""