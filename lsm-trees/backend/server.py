from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from lsm import LSMTree
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lsm_tree = LSMTree(memtable_threshold=5)

class SetRequest(BaseModel):
    key: str
    value: str

class DeleteRequest(BaseModel):
    key: str

@app.post("/set")
def set_key(item: SetRequest):
    lsm_tree.set(item.key, item.value)
    return {"status": "ok"}

@app.post("/delete")
def delete_key(item: DeleteRequest):
    lsm_tree.delete(item.key)
    return {"status": "ok"}

@app.get("/get")
def get_key(key: str):
    value = lsm_tree.get(key)
    return {"key": key, "value": value}

@app.get("/data")
def get_data():
    memtable_data = lsm_tree.memtable.data
    sstables_data = []
    for sstable in lsm_tree.sstables:
        with open(sstable, "r") as f:
            data = [json.loads(line) for line in f]
            sstables_data.append(data)
    return {"memtable": memtable_data, "sstables": sstables_data}

@app.post("/clear")
def clear_tree():
    global lsm_tree
    lsm_tree = LSMTree(memtable_threshold=5)
    return {"status": "cleared"}
