# Operational Transformation API

This project provides a backend API for a simple Operational Transformation (OT) implementation, demonstrating how collaborative editing can be achieved. The API is built using Python and FastAPI.

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

The OT API provides the following endpoints for managing a shared document.

### Operation Model

Represents an operation to be applied to the document.

```json
{
  "op_type": "insert",
  "pos": 0,
  "text": "a"
}
```

- `op_type`: "insert" or "delete".
- `pos`: The position of the operation.
- `text`: The text to insert or delete.

### Endpoints

#### `GET /document`

Returns the current state of the document.

- **Response:** `{"document": "..."}`

**cURL Example:**

```bash
curl -X GET "http://127.0.0.1:8000/document"
```

#### `POST /apply`

Applies an operation to the document.

- **Request Body:** `OperationModel`
- **Response:** The updated document state.

**cURL Example (Insert):**

```bash
curl -X POST "http://127.0.0.1:8000/apply" \
     -H "Content-Type: application/json" \
     -d '{"op_type": "insert", "pos": 5, "text": " beautiful"}'
```

**cURL Example (Delete):**

```bash
curl -X POST "http://127.0.0.1:8000/apply" \
     -H "Content-Type: application/json" \
     -d '{"op_type": "delete", "pos": 0, "text": "Hello, "}'
```

#### `POST /reset`

Resets the document to its original state.

- **Response:** `{"message": "Document reset successfully."}`

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/reset"
```

## Concurrent Operations and Conflict Resolution

The server can handle a batch of concurrent operations via the `/apply-batch` endpoint. The operations in the batch are transformed against each other to ensure consistency.

### Insert-Insert Conflict

If two users insert text at the same position, the server will transform the operations so that one insertion follows the other. The final order depends on the order in which the operations are processed in the batch.

**Example:**

- **Initial Document:** `Hello, world!`
- **User 1 sends:** `{"op_type": "insert", "pos": 7, "text": " beautiful"}`
- **User 2 sends:** `{"op_type": "insert", "pos": 7, "text": " amazing"}`

If User 1's operation is processed first, the final document will be: `Hello, beautiful amazing world!`

### Insert-Delete Conflict

If one user inserts text at a position that another user is deleting, the transformation logic will adjust the operations to preserve the user's intent.

**Example:**

- **Initial Document:** `Hello, world!`
- **User 1 sends:** `{"op_type": "insert", "pos": 7, "text": "new "}`
- **User 2 sends:** `{"op_type": "delete", "pos": 0, "text": "Hello, "}`

If User 2's deletion is processed first, the document becomes `world!`. User 1's insertion at position 7 is transformed to position 0, resulting in the final document: `new world!`

### Delete-Delete Conflict

If two users delete overlapping text, the transformation logic will ensure that the correct text is removed without errors.

**Example:**

- **Initial Document:** `Hello, beautiful world!`
- **User 1 sends:** `{"op_type": "delete", "pos": 7, "text": "beautiful "}`
- **User 2 sends:** `{"op_type": "delete", "pos": 0, "text": "Hello, "}`

If User 2's operation is processed first, the document becomes `beautiful world!`. User 1's deletion at position 7 is transformed to position 0, resulting in the final document: `world!`

### Delete-Insert Conflict

If one user deletes a range of text and another user inserts text within that range, the insertion will be effectively ignored because the text it was relative to has been removed.

**Example:**

- **Initial Document:** `Hello, world!`
- **User 1 sends:** `{"op_type": "delete", "pos": 0, "text": "Hello, world!"}`
- **User 2 sends:** `{"op_type": "insert", "pos": 7, "text": "new "}`

If User 1's deletion is processed first, the document becomes empty. User 2's insertion will be transformed, but since its context is gone, it may be discarded or handled based on the specific transformation function logic. In our case, the transformation will likely result in a `insert` operation, and the final document will be 'new'.

If User 2's insertion is processed first, the document becomes `Hello, new world!`. User 1's deletion of "Hello, world!" will be transformed. However, with our current simple transformation logic, this scenario is treated as an ambiguous overlap, and the deletion operation is discarded. This would result in a final document of `Hello, new world!`.
