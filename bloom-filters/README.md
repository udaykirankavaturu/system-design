# Bloom Filter API

This project provides a backend API for a Bloom Filter implementation, a probabilistic data structure used to test whether an element is a member of a set. The API is built using Python and FastAPI.

## How it Works

A Bloom filter is a bit array of *m* bits, initially all set to 0. It uses *k* different hash functions, each of which maps or hashes some set element to one of the *m* array positions with a uniform random distribution.

- **To add an item:** The item is fed to each of the *k* hash functions to get *k* array positions. The bits at all these positions are set to 1.
- **To check an item:** The item is fed to each of the *k* hash functions to get *k* array positions. If any of the bits at these positions are 0, the element is definitely not in the set. If all are 1, then the element may be in the set.

This means the filter can have false positives but not false negatives.

## Hash Function Implementation

This implementation uses a fixed set of four hash functions to populate the bit array. This approach is common in real-world scenarios where a specific number of hash functions is chosen to balance performance and accuracy.

The hash functions used are:

- **MD5**: A widely used cryptographic hash function.
- **Murmur3**: A popular non-cryptographic hash function known for its speed and good distribution.
- **xxHash**: An extremely fast non-cryptographic hash function.
- **FNV-1a 32-bit**: A simple and effective non-cryptographic hash function.

For each item added to the filter, all four hash functions are applied to it, and the corresponding bits in the array are set to 1.

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

This will install FastAPI, Uvicorn, and the required hash function libraries.

## Running the Server

Once the setup is complete and your virtual environment is activated, you can start the FastAPI server.

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reloading of the server on code changes, which is useful for development.
The API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs` and the alternative ReDoc documentation at `http://127.0.0.1:8000/redoc`.

## API Documentation

The Bloom Filter API provides the following endpoints.

### Item Model

Represents an item to be added to or checked in the filter.

```json
{
  "item": "my_item"
}
```

### Endpoints

#### `POST /add`

Adds an item to the Bloom filter.

- **Request Body:** `Item`
- **Response:** `{"message": "'<item>' added to the bloom filter."}`

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/add" \
     -H "Content-Type: application/json" \
     -d '{"item": "hello"}'
```

#### `POST /check`

Checks if an item may be in the Bloom filter.

- **Request Body:** `Item`
- **Response:** `{"item": "<item>", "possibly_exists": true/false}`

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"item": "world"}'
```

#### `GET /status`

Returns the current state of the bloom filter, including the bit array and the number of hash functions used.

- **Response:** `{"bit_array": [0, 1, ...], "hash_count": 4}`

**cURL Example:**

```bash
curl -X GET "http://127.0.0.1:8000/status"
```

#### `POST /reset`

Resets the Bloom filter to its initial empty state.

- **Response:** `{"message": "Bloom filter has been reset."}`

**cURL Example:**

```bash
curl -X POST "http://127.0.0.1:8000/reset"
```

## Interacting with the UI

1.  **Start the backend server** as described above.
2.  **Open the `frontend/index.html` file** in your web browser.

- **Enter an item** in the input box.
- **Click "Add"** to add the item to the Bloom filter.
- **Click "Check"** to see if the item might be in the filter.
- **Click "Reset"** to clear the Bloom filter.

