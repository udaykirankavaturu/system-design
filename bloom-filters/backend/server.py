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

# Initialize Bloom Filter
bloom_filter = BloomFilter(size=100)

@app.post("/add")
def add_item(item: Item):
    """Adds an item to the bloom filter."""
    bloom_filter.add(item.item)
    return {"message": f"'{item.item}' added to the bloom filter."}

@app.post("/check")
def check_item(item: Item):
    """Checks if an item may be in the bloom filter."""
    possibly_exists = bloom_filter.check(item.item)
    return {"item": item.item, "possibly_exists": possibly_exists}

@app.get("/status")
def get_status():
    """Returns the current state of the bloom filter."""
    return {"bit_array": bloom_filter.bit_array, "hash_count": bloom_filter.hash_count}

@app.post("/reset")
def reset_filter():
    """Resets the bloom filter to its initial empty state."""
    global bloom_filter
    bloom_filter = BloomFilter(size=100)
    return {"message": "Bloom filter has been reset."}
