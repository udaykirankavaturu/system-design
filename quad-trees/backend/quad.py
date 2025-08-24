from typing import List, Optional

class Point:
    def __init__(self, longitude, latitude, label=None):
        self.x = longitude
        self.y = latitude
        self.label = label
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        if self.label:
            return f"Point(label='{self.label}', x={self.x}, y={self.y})"
        return f"Point(x={self.x}, y={self.y})"
        
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

        # Check if the point exists in this node's points, considering label if provided
        found_in_this_node = False
        for i, p in enumerate(self.points):
            if p.x == point.x and p.y == point.y:
                # If a label is provided in the point to delete, it must match
                # Otherwise, if no label is provided, just match by coordinates
                if point.label is None or p.label == point.label:
                    self.points.pop(i)
                    found_in_this_node = True
                    break
        
        if found_in_this_node:
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

    def to_dict(self):
        node_data = {
            "boundary": {
                "x": self.boundary.x,
                "y": self.boundary.y,
                "w": self.boundary.w,
                "h": self.boundary.h
            },
            "points": [{"longitude": p.x, "latitude": p.y, "label": p.label} for p in self.points],
            "divided": self.divided
        }
        if self.divided:
            node_data["children"] = {
                "northeast": self.northeast.to_dict() if self.northeast else None,
                "northwest": self.northwest.to_dict() if self.northwest else None,
                "southeast": self.southeast.to_dict() if self.southeast else None,
                "southwest": self.southwest.to_dict() if self.southwest else None,
            }
        return node_data
