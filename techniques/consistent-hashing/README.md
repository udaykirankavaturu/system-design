# Consistent Hashing API

This project provides a backend API for a Consistent Hashing implementation, allowing for efficient distribution of keys among a set of servers. The API is built using Python and FastAPI.

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

The Consistent Hashing API provides the following endpoints for managing servers and keys.

### Server Model

Represents a server to be added or removed from the hash ring.

```json
{
  "server_name": "server1"
}
```

### Key Model

Represents a key to be mapped to a server.

```json
{
  "key": "my_key"
}
```

### Endpoints

#### `POST /servers/`

Adds a new server to the consistent hash ring.

- **Request Body:** `ServerModel`
- **Response:** `{"message": "Server added successfully."}`
- **Status Codes:**
  - `201 Created`: Server successfully added.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/servers/" \
     -H "Content-Type: application/json" \
     -d '{"server_name": "server1"}'
```

#### `DELETE /servers/`

Removes a server from the consistent hash ring.

- **Request Body:** `ServerModel`
- **Response:** `{"message": "Server removed successfully."}`
- **Status Codes:**
  - `200 OK`: Server successfully removed.
  - `404 Not Found`: Server not found in the hash ring.

**cURL Example:**

```bash
curl -X DELETE "http://127.0.0.1:8000/servers/" \
     -H "Content-Type: application/json" \
     -d '{"server_name": "server1"}'
```

#### `POST /keys/`

Finds which server a key is mapped to.

- **Request Body:** `KeyModel`
- **Response:** `{"server": "server_name"}`
- **Status Codes:**
  - `200 OK`: Server found for the key.
  - `404 Not Found`: No servers available in the hash ring.

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/keys/" \
     -H "Content-Type: application/json" \
     -d '{"key": "user_profile_123"}'
```

#### `GET /ring/`

Returns a JSON representation of the current consistent hash ring structure for visualization.

- **Response:** A JSON object representing the hash ring, including server positions.

**cURL Example:**

```bash
curl -X GET "http://127.0.0.1:8000/ring/"
```

```