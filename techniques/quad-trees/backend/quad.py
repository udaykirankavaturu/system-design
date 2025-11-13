from typing import List, Optional

# Represents a single point in 2D space, typically used for geographical coordinates.
class Point:
    def __init__(self, longitude, latitude, label=None):
        """
        Initializes a Point object.

        Args:
            longitude (float): The x-coordinate of the point.
            latitude (float): The y-coordinate of the point.
            label (str, optional): An optional label or name for the point. Defaults to None.
        """
        self.x = longitude
        self.y = latitude
        self.label = label
        
    def __eq__(self, other):
        """
        Compares two Point objects for equality based on their coordinates.
        Labels are not considered for equality in this implementation.
        """
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        """
        Returns a string representation of the Point object.
        Includes the label if present.
        """
        if self.label:
            return f"Point(label='{self.label}', x={self.x}, y={self.y})"
        return f"Point(x={self.x}, y={self.y})"
        
# Represents a rectangular boundary in 2D space, defined by its center and half-dimensions.
class Rectangle:
    def __init__(self, x, y, w, h):
        """
        Initializes a Rectangle object.

        Args:
            x (float): The x-coordinate of the center of the rectangle.
            y (float): The y-coordinate of the center of the rectangle.
            w (float): Half the width of the rectangle (e.g., half longitude degrees).
            h (float): Half the height of the rectangle (e.g., half latitude degrees).
        """
        # (x,y) is center of rectangle (longitude, latitude)
        self.x = x
        self.y = y
        self.w = w  # half width (longitude degrees)
        self.h = h  # half height (latitude degrees)
        
    def contains(self, point):
        """
        Checks if a given Point is within the bounds of this Rectangle.

        Args:
            point (Point): The point to check.

        Returns:
            bool: True if the point is within the rectangle, False otherwise.
        """
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)
    
    def intersects(self, range):
        """
        Checks if this Rectangle intersects with another given Rectangle.

        Args:
            range (Rectangle): The other rectangle to check for intersection.

        Returns:
            bool: True if the rectangles intersect, False otherwise.
        """
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y - range.h < self.y - self.h)

# Implements a QuadTree data structure for efficient spatial partitioning of points.
class QuadTree:
    def __init__(self, boundary: Rectangle, capacity: int):
        """
        Initializes a QuadTree node.

        Args:
            boundary (Rectangle): The rectangular area this QuadTree node covers.
            capacity (int): The maximum number of points this node can hold before subdividing.
        """
        self.boundary: Rectangle = boundary
        self.capacity: int = capacity
        self.points: List[Point] = []  # List of points directly within this node
        self.divided: bool = False     # True if this node has been subdivided
        # Child QuadTree nodes for the four quadrants
        self.northeast: Optional['QuadTree'] = None
        self.northwest: Optional['QuadTree'] = None
        self.southeast: Optional['QuadTree'] = None
        self.southwest: Optional['QuadTree'] = None
        
    def subdivide(self):
        """
        Divides this QuadTree node into four smaller QuadTree nodes (quadrants).
        This method is called when the node's capacity is exceeded.
        """
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2
        
        # Create new Rectangles for each quadrant
        self.northeast = QuadTree(Rectangle(x + w, y - h, w, h), self.capacity)
        self.northwest = QuadTree(Rectangle(x - w, y - h, w, h), self.capacity)
        self.southeast = QuadTree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.southwest = QuadTree(Rectangle(x - w, y + h, w, h), self.capacity)
        self.divided = True
        
    def insert(self, point):
        """
        Inserts a point into the QuadTree.

        Args:
            point (Point): The point to insert.

        Returns:
            bool: True if the point was successfully inserted, False if it's outside the boundary.
        """
        # If the point is not within this QuadTree's boundary, it cannot be inserted here.
        if not self.boundary.contains(point):
            return False
        
        # If this node has capacity, add the point directly.
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            # If capacity is exceeded, subdivide if not already divided.
            if not self.divided:
                self.subdivide()
            
            # Attempt to insert the point into one of the child quadrants.
            # The point will only fit into one child's boundary.
            if self.northeast and self.northeast.insert(point):
                return True
            if self.northwest and self.northwest.insert(point):
                return True
            if self.southeast and self.southeast.insert(point):
                return True
            if self.southwest and self.southwest.insert(point):
                return True
        return False # Should not be reached if point is within boundary and tree is correctly structured
        
    def query(self, range: Rectangle, found: List[Point]):
        """
        Finds all points within a given rectangular range.

        Args:
            range (Rectangle): The search area.
            found (List[Point]): A list to append the found points to.
        """
        # If the search range does not intersect this node's boundary, no points can be found here.
        if not self.boundary.intersects(range):
            return
        else:
            # Check points directly in this node.
            for p in self.points:
                if range.contains(p):
                    found.append(p)
            
            # If this node is subdivided, recursively query its children.
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
        """
        Deletes a specific point from the QuadTree.
        Deletion is based on coordinates. If a label is provided in the 'point' argument,
        it must also match for the point to be deleted.

        Args:
            point (Point): The point to delete.

        Returns:
            bool: True if the point was found and deleted, False otherwise.
        """
        # If the point is not within this QuadTree's boundary, it cannot be here.
        if not self.boundary.contains(point):
            return False

        # Check if the point exists in this node's points, considering label if provided.
        found_in_this_node = False
        for i, p in enumerate(self.points):
            if p.x == point.x and p.y == point.y:
                # If a label is provided in the point to delete, it must match.
                # Otherwise, if no label is provided, just match by coordinates.
                if point.label is None or p.label == point.label:
                    self.points.pop(i) # Remove the point
                    found_in_this_node = True
                    break
        
        if found_in_this_node:
            # If this node is now empty and its children are also empty, collapse them
            # to maintain an efficient tree structure.
            if not self.points and self.divided and self._are_children_empty():
                self._collapse_children()
            return True
        elif self.divided:
            # If not found in this node, and this node is divided,
            # attempt to delete from one of the child quadrants.
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
        """
        Helper method to check if all child quadrants are empty (contain no points and are not subdivided).

        Returns:
            bool: True if all children are empty, False otherwise.
        """
        children = [self.northeast, self.northwest, self.southeast, self.southwest]
        for child in children:
            # A child is not empty if it exists AND (it's divided OR it contains points)
            if child is not None and (child.divided or child.points):
                return False
        return True


    def _collapse_children(self):
        """
        Helper method to collapse (remove) child quadrants.
        This is called when a node and all its children become empty,
        optimizing the tree by removing unnecessary subdivisions.
        """
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def _check_and_collapse_children_after_delete(self):
        """
        Helper method to check if a node's children can be collapsed after a deletion.
        This ensures the tree remains optimized.
        """
        if not self.points and self.divided and self._are_children_empty():
            self._collapse_children()

    def to_dict(self):
        """
        Converts the QuadTree (and its sub-trees) into a dictionary representation.
        Useful for serialization (e.g., to JSON) for visualization or API responses.

        Returns:
            dict: A dictionary representing the QuadTree node and its children.
        """
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