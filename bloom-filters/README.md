# Bloom Filter API

This project provides a backend API for a Bloom Filter implementation, a probabilistic data structure used to test whether an element is a member of a set. The API is built using Python and FastAPI.

## How it Works

A Bloom filter is a bit array of *m* bits, initially all set to 0. It uses *k* different hash functions, each of which maps or hashes some set element to one of the *m* array positions with a uniform random distribution.

- **To add an item:** The item is fed to each of the *k* hash functions to get *k* array positions. The bits at all these positions are set to 1.
- **To check an item:** The item is fed to each of the *k* hash functions to get *k* array positions. If any of the bits at these positions are 0, the element is definitely not in the set. If all are 1, then the element may be in the set.

This means the filter can have false positives but not false negatives.

## Hash Function Implementation

To generate multiple hash values, this implementation uses a common technique. Instead of implementing *k* different hash functions, we use a single cryptographic hash function (`MD5`) and combine it with a simple iterative process.

For each item, the `_hashes` method iterates from `0` to `hash_count - 1`. In each iteration, it concatenates the item with the current iteration number, hashes the result using MD5, and then takes the modulo with the filter size to get an index within the bit array.

This approach simulates the behavior of *k* independent hash functions without the complexity of designing and implementing them separately.

In real-world applications, while this iterative approach is valid, the choice of hash function is critical for performance. Cryptographic hash functions like MD5 are generally slower than needed. Production-grade Bloom filters often use fast, non-cryptographic hash functions such as:

- **MurmurHash**: A popular choice known for its speed and good distribution.
- **xxHash**: An extremely fast hash function, often used in high-performance scenarios.
- **Fowler-Noll-Vo (FNV)**: A simple and effective hash function that is also very fast.

These functions are designed to be computationally inexpensive while still providing a uniform distribution of hash values, which is essential for the efficiency of the Bloom filter.

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

This will install FastAPI and Uvicorn.

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

Returns the current state of the bloom filter's bit array.

- **Response:** `{"bit_array": [0, 1, 0, ..., 1]}`

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
- **Click "Add"** to add the item to the Bloom filter. The bit array below will update.
- **Click "Check"** to see if the item might be in the filter.
- **Click "Reset"** to clear the Bloom filter.