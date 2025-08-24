from typing import List, Optional

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
                    range.y - range.h < self.y - self.h)

class QuadTree:
    def __init__(self, boundary: Rectangle, capacity: int):
        self.boundary: Rectangle = boundary
        self.capacity: int = capacity
        self.points: List[Point] = []
        self.divided: bool = False
        self.northeast: Optional['QuadTree'] = None
        self.northwest: Optional['QuadTree'] = None
        self.southeast: Optional['QuadTree'] = None
        self.southwest: Optional['QuadTree'] = None
        
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
            if self.northeast and self.northeast.insert(point):
                return True
            if self.northwest and self.northwest.insert(point):
                return True
            if self.southeast and self.southeast.insert(point):
                return True
            if self.southwest and self.southwest.insert(point):
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
                if self.northwest:
                    self.northwest.query(range, found)
                if self.northeast:
                    self.northeast.query(range, found)
                if self.southwest:
                    self.southwest.query(range, found)
                if self.southeast:
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
            if self.northeast and self.northeast.delete(point):
                return True
            if self.northwest and self.northwest.delete(point):
                return True
            if self.southeast and self.southeast.delete(point):
                return True
            if self.southwest and self.southwest.delete(point):
                return True
            # After attempting to delete from children, if a child node becomes empty
            # and its siblings are also empty, and this parent node is also empty,
            # then collapse the children.
            self._check_and_collapse_children_after_delete()
        return False

    def _are_children_empty(self):
        children = [self.northeast, self.northwest, self.southeast, self.southwest]
        for child in children:
            if child is None or child.divided or child.points:
                return False
        return True


    def _collapse_children(self):
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def _check_and_collapse_children_after_delete(self):
        if not self.points and self.divided and self._are_children_empty():
            self._collapse_children()

# Usage example for Hyderabad

hyderabad_boundary = Rectangle(x=78.5, y=17.4, w=0.25, h=0.25)
qt = QuadTree(hyderabad_boundary, 4)

drivers = [
    Point(78.48, 17.42),
    Point(78.52, 17.46),
    Point(78.49, 17.38),
    Point(78.53, 17.41),
    Point(78.47, 17.44)
]

for d in drivers:
    qt.insert(d)

# Search drivers near a rider
query_region = Rectangle(x=78.50, y=17.40, w=0.05, h=0.05)
found_drivers = []
qt.query(query_region, found_drivers)
print("Nearby drivers before delete:", found_drivers)

# Delete a driver
qt.delete(Point(78.49, 17.38))

found_drivers_after_delete = []
qt.query(query_region, found_drivers_after_delete)
print("Nearby drivers after delete:", found_drivers_after_delete)
