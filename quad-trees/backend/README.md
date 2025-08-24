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
