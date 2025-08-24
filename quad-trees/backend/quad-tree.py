class Point:
    def __init__(self, longitude, latitude):
        self.x = longitude
        self.y = latitude
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
        
class Rectangle:
    def __init__(self, x, y, w, h):
        # (x,y) is center of rectangle (longitude, latitude)
        self.x = x
        self.y = y
        self.w = w  # half width (longitude degrees)
        self.h = h  # half height (latitude degrees)
        
    def contains(self, point):
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)
    
    def intersects(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2
        
        self.northeast = QuadTree(Rectangle(x + w, y - h, w, h), self.capacity)
        self.northwest = QuadTree(Rectangle(x - w, y - h, w, h), self.capacity)
        self.southeast = QuadTree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.southwest = QuadTree(Rectangle(x - w, y + h, w, h), self.capacity)
        self.divided = True
        
    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northeast.insert(point):
                return True
            if self.northwest.insert(point):
                return True
            if self.southeast.insert(point):
                return True
            if self.southwest.insert(point):
                return True
        return False
        
    def query(self, range, found):
        if not self.boundary.intersects(range):
            return
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)

    def delete(self, point):
        if not self.boundary.contains(point):
            return False

        if point in self.points:
            self.points.remove(point)
            # If this node is now empty, and its children are also empty, collapse them.
            if not self.points and self.divided and self._are_children_empty():
                self._collapse_children()
            return True
        elif self.divided:
            return (self.northeast.delete(point) or
                    self.northwest.delete(point) or
                    self.southeast.delete(point) or
                    self.southwest.delete(point))
        return False

    def _are_children_empty(self):
        return all(not child.divided and not child.points for child in [
            self.northeast, self.northwest, self.southeast, self.southwest])

    def _collapse_children(self):
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
