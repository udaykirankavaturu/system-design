import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Import the QuadTree implementation from your file
from quad_tree import Point, Rectangle, QuadTree

# --- Pydantic Models for API data validation ---

class PointModel(BaseModel):
    longitude: float
    latitude: float

class RectangleModel(BaseModel):
    # Center of the rectangle
    x: float
    y: float
    # Half-width and half-height
    w: float
    h: float

# --- FastAPI App Initialization ---

app = FastAPI(
    title="QuadTree API",
    description="An API to interact with a QuadTree for geospatial data.",
    version="1.0.0",
)

# --- Global QuadTree Instance ---
# Define a boundary for our QuadTree.
# Example: A boundary roughly covering a large city area.
world_boundary = Rectangle(0, 0, 180, 90) # Covers the entire globe
# The capacity of each node in the tree.
CAPACITY = 4
# Initialize the QuadTree. This will act as our in-memory database.
quad_tree = QuadTree(world_boundary, CAPACITY)


# --- API Endpoints ---

@app.post("/points/", status_code=201, response_model=PointModel, tags=["Points"])
def insert_point(point: PointModel):
    """
    Inserts a new geographical point into the QuadTree.
    """
    p = Point(point.longitude, point.latitude)
    if not quad_tree.insert(p):
        raise HTTPException(
            status_code=400,
            detail="Point is outside the boundary of the QuadTree."
        )
    return point

@app.post("/points/search/", response_model=List[PointModel], tags=["Points"])
def search_points(range_rect: RectangleModel):
    """
    Searches for points within a given rectangular range.
    """
    search_range = Rectangle(range_rect.x, range_rect.y, range_rect.w, range_rect.h)
    found_points = []
    quad_tree.query(search_range, found_points)
    # Convert internal Point objects to Pydantic models for the response
    return [{"longitude": p.x, "latitude": p.y} for p in found_points]

@app.delete("/points/", status_code=200, tags=["Points"])
def delete_point(point: PointModel):
    """
    Deletes a geographical point from the QuadTree.
    """
    p = Point(point.longitude, point.latitude)
    if not quad_tree.delete(p):
        raise HTTPException(
            status_code=404,
            detail="Point not found in the QuadTree."
        )
    return {"message": "Point deleted successfully."}
