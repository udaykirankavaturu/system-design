from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bloom import BloomFilter

app = FastAPI()

# Allow CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    item: str

# Initialize Bloom Filter and history
bloom_filter = BloomFilter(size=100)
history = []

@app.post("/add")
def add_item(item: Item):
    """Adds an item to the bloom filter, stores it in history, and returns the generated hashes."""
    hashes = bloom_filter.add(item.item)
    history.append({"item": item.item, "hashes": hashes})
    return {"message": f"'{item.item}' added to the bloom filter.", "hashes": hashes}

@app.post("/check")
def check_item(item: Item):
    """Checks if an item may be in the bloom filter and returns the generated hashes."""
    possibly_exists, hashes = bloom_filter.check(item.item)
    return {"item": item.item, "possibly_exists": possibly_exists, "hashes": hashes}

@app.get("/status")
def get_status():
    """Returns the current state of the bloom filter."""
    return {"bit_array": bloom_filter.bit_array, "hash_count": bloom_filter.hash_count}

@app.get("/history")
def get_history():
    """Returns the history of added items."""
    return {"history": history}

@app.post("/reset")
def reset_filter():
    """Resets the bloom filter and history to their initial empty state."""
    global bloom_filter, history
    bloom_filter = BloomFilter(size=100)
    history = []
    return {"message": "Bloom filter and history have been reset."}
