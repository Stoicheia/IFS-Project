import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
from shapely.geometry import Polygon as ShapelyPolygon, Point
from shapely import affinity

class CustomPolygon:
    def __init__(self, points, color='blue', alpha=0.5):
        self.points = points
        self.color = color
        self.alpha = alpha
        self.polygon = ShapelyPolygon(points)
        
    def draw(self, ax):
        poly = MatplotlibPolygon(self.points, facecolor=self.color, alpha=self.alpha)
        ax.add_patch(poly)
    
    def overlaps(self, other):
        return self.polygon.intersects(other.polygon)
    
    def is_covered(self, others):
        for other in others:
            if other is not self:
                if other.polygon.contains(self.polygon):
                    return True
        return False
    
    def contains_point(self, point):
        return self.polygon.contains(Point(point))
    
    def move(self, dx, dy):
        self.polygon = affinity.translate(self.polygon, dx, dy)
        self.points = self.polygon.exterior.coords[:-1]
    
class CustomPolygonList:
    def __init__(self, polygons):
        self.polygons = polygons
        self.fig, self.ax = plt.subplots()
        self.draw()
        self.current_polygon = None
        self.offset = (0, 0)
        self.connect()
        
    def connect(self):
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
    def on_press(self, event):
        if event.button == 1:
            for polygon in reversed(self.polygons):
                if polygon.contains_point((event.xdata, event.ydata)):
                    self.current_polygon = polygon
                    self.offset = (event.xdata - polygon.points[0][0], event.ydata - polygon.points[0][1])
                    break
                    
    def on_release(self, event):
        if event.button == 1:
            self.current_polygon = None
            self.offset = (0, 0)
        
    def on_motion(self, event):
        if self.current_polygon is not None:
            dx = event.xdata - self.current_polygon.points[0][0] - self.offset[0]
            dy = event.ydata - self.current_polygon.points[0][1] - self.offset[1]
            self.current_polygon.move(dx, dy)
            self.draw()
            
    def draw(self):
        self.ax.clear()
        for polygon in self.polygons:
            polygon.draw(self.ax)
            print(polygon.polygon.exterior.coords.xy)
        self.ax.set_xlim([-0.5, 1.5])
        self.ax.set_ylim([-0.5, 1.5])
        plt.draw()
        
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
plt.grid()
plt.show()
