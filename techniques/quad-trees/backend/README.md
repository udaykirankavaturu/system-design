# QuadTree API

This project provides a backend API for a QuadTree data structure, allowing for efficient geospatial queries. The API is built using Python and FastAPI.

## Local Development Setup

Follow these steps to set up a local development environment and run the server.

### 1. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies. Navigate to the `backend` directory in your terminal and run the following command to create a virtual environment named `venv`:

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

Before installing dependencies, you need to activate the environment.

**On macOS and Linux:**

```bash
source venv/bin/activate
```

**On Windows:**

```bash
.\venv\Scripts\activate
```

Your terminal prompt should now be prefixed with `(venv)`, indicating that the virtual environment is active.

### 3. Install Requirements

With the virtual environment active, install the necessary Python packages using the `requirements.txt` file:

```bash
pip3 install -r requirements.txt
```

This will install FastAPI and Uvicorn, the two dependencies required to run the server.

## Running the Server

Once the setup is complete and your virtual environment is activated, you can start the FastAPI server.

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reloading of the server on code changes, which is useful for development.
The API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs` and the alternative ReDoc documentation at `http://127.0.0.1:8000/redoc`.

## API Documentation

The QuadTree API provides the following endpoints for managing and querying geographical points.

### Point Model

Represents a geographical point.

```json
{
  "longitude": 0.0,
  "latitude": 0.0
}
```

### Rectangle Model

Represents a rectangular area for search queries.

```json
{
  "x": 0.0,
  "y": 0.0,
  "w": 0.0,
  "h": 0.0
}
```

- `x`, `y`: Center coordinates of the rectangle.
- `w`, `h`: Half-width and half-height of the rectangle.

### Endpoints

#### `POST /points/`

Inserts a new geographical point into the QuadTree.

- **Request Body:** `PointModel`
- **Response:** `PointModel` of the inserted point.
- **Status Codes:**
  - `201 Created`: Point successfully inserted.
  - `400 Bad Request`: Point is outside the defined QuadTree boundary.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/points/"
     -H "Content-Type: application/json"
     -d '{"longitude": 78.48, "latitude": 17.42}'
```

#### `POST /points/search/`

Searches for points within a given rectangular range.

- **Request Body:** `RectangleModel`
- **Response:** `List[PointModel]` containing all points found within the specified range.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/points/search/"
     -H "Content-Type: application/json"
     -d '{"x": 78.50, "y": 17.40, "w": 0.05, "h": 0.05}'
```

#### `DELETE /points/`

Deletes a geographical point from the QuadTree.

- **Request Body:** `PointModel`
- **Response:** `{"message": "Point deleted successfully."}` on success.
- **Status Codes:**
  - `200 OK`: Point successfully deleted.
  - `404 Not Found`: Point not found in the QuadTree.

**cURL Example:**

```bash
curl -X DELETE "http://127.0.0.1:8000/points/"
     -H "Content-Type: application/json"
     -d '{"longitude": 78.49, "latitude": 17.38}'
```

#### `GET /quadtree/visualize/`

Returns a JSON representation of the current QuadTree structure for visualization.

- **Response:** A nested JSON object representing the QuadTree, including boundaries, points, and children nodes.

**cURL Example:**

```bash
curl -X GET "http://127.0.0.1:8000/quadtree/visualize/"
```

## Usage Examples

Let\\'s add some example nodes in Hyderabad city and then perform a search operation.

### 1. Insert Example Points (Hyderabad Landmarks)

Here are a few famous landmarks in Hyderabad with their approximate longitude and latitude.

- **Charminar:** 17.3616, 78.4747
- **Golconda Fort:** 17.3800, 78.4018
- **Hitech City:** 17.4486, 78.3833
- **Gachibowli:** 17.4486, 78.3433
- **Secunderabad Railway Station:** 17.4399, 78.5000

You can insert these points using the following `curl` commands:

```bash
# Insert Charminar
curl -X POST "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.4747, "latitude": 17.3616}'

# Insert Golconda Fort
curl -X POST "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.4018, "latitude": 17.3800}'

# Insert Hitech City
curl -X POST "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.3833, "latitude": 17.4486}'

# Insert Gachibowli
curl -X POST "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.3433, "latitude": 17.4486}'

# Insert Secunderabad Railway Station
curl -X POST "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.5000, "latitude": 17.4399}'
```

### 2. Search for Points within a Range

Now, let\'s search for points within a rectangular area that covers some of the inserted points. For example, a search around the central-western part of Hyderabad, which might include Golconda Fort, Hitech City, and Gachibowli.

Let\'s define a search rectangle:

- **Center (x, y):** 78.39, 17.41 (roughly between Golconda and Hitech City)
- **Half-width (w):** 0.047 (about 10 km width)
- **Half-height (h):** 0.045 (about 10 km height)

This rectangle would cover longitudes from `78.31` to `78.47` and latitudes from `17.36` to `17.46`.

```bash
# Search for points in a specific area
curl -X POST "http://127.0.0.1:8000/points/search/" \
     -H "Content-Type: application/json" \
     -d '{"x": 78.39, "y": 17.41, "w": 0.08, "h": 0.05}'
```

This search should return Golconda Fort, Hitech City, and Gachibowli, as their coordinates fall within this range.

### 3. Delete an Example Point

You can also delete a specific point. For instance, to delete Charminar:

```bash
# Delete Charminar
curl -X DELETE "http://127.0.0.1:8000/points/" \
     -H "Content-Type: application/json" \
     -d '{"longitude": 78.4747, "latitude": 17.3616}'
```
