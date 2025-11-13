import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

from ch import ConsistentHashing

class NodeModel(BaseModel):
    name: str

class KeyModel(BaseModel):
    key: str

app = FastAPI(
    title="Consistent Hashing API",
    description="An API to interact with a Consistent Hashing implementation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Consistent Hashing ring
ch = ConsistentHashing(num_replicas=3)

@app.post("/nodes/", status_code=201, tags=["Nodes"])
def add_node(node: NodeModel):
    """
    Adds a new node to the consistent hashing ring.
    """
    ch.add_node(node.name)
    return {"message": f"Node '{node.name}' added successfully."}

@app.delete("/nodes/{node_name}", status_code=200, tags=["Nodes"])
def remove_node(node_name: str):
    """
    Removes a node from the consistent hashing ring.
    """
    ch.remove_node(node_name)
    return {"message": f"Node '{node_name}' removed successfully."}

@app.get("/nodes/", response_model=List[str], tags=["Nodes"])
def get_nodes():
    """
    Gets all unique nodes in the ring.
    """
    if not ch.hash_ring:
        return []
    return sorted(list(set(ch.hash_ring.values())))

@app.get("/keys/{key}", tags=["Keys"])
def get_node_for_key(key: str):
    """
    Gets the node that a specific key is mapped to.
    """
    if not ch.hash_ring:
        raise HTTPException(status_code=404, detail="Hash ring is empty.")
    node = ch.get_node(key)
    return {"key": key, "node": node}

@app.get("/ring/", tags=["Ring"])
def get_ring():
    """
    Returns a representation of the current hash ring for visualization.
    """
    return {
        "num_replicas": ch.num_replicas,
        "sorted_hashes": ch._sorted_hashes,
        "hash_ring": ch.hash_ring
    }
