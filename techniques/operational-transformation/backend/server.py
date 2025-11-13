import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Import the OT implementation from your file
from ot import Operation, apply_operation, transform

# --- Pydantic Models for API data validation ---

class OperationModel(BaseModel):
    op_type: str
    pos: int
    text: Optional[str] = None

# --- FastAPI App Initialization ---

app = FastAPI(
    title="Operational Transformation API",
    description="An API to interact with a simple OT implementation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models for API data validation ---

class OperationRequest(BaseModel):
    op: OperationModel
    revision: int

# --- Global State ---
# We now store the document and its revision in a single dictionary.
document_state = {
    "doc": "Hello, world!",
    "revision": 0
}
# History stores the sequence of operations applied to the document.
history: List[Operation] = []


# --- API Endpoints ---

@app.get("/")
async def read_index():
    return FileResponse('../frontend/index.html')

@app.get("/document", tags=["Document"])
def get_document():
    """
    Returns the current state of the document and its revision.
    """
    return document_state

@app.post("/apply-operation", tags=["Operations"])
def apply_operation_endpoint(request: OperationRequest):
    """
    Applies a single operation to the document, transforming it if necessary.
    """
    global document_state, history
    
    client_op = Operation(request.op.op_type, request.op.pos, request.op.text or "")
    client_revision = request.revision
    
    server_revision = document_state["revision"]
    
    # If the client's revision is out of date, we need to transform the operation.
    if client_revision < server_revision:
        # Get all operations that the client hasn't seen yet.
        concurrent_ops = history[client_revision:]
        for concurrent_op in concurrent_ops:
            client_op = transform(client_op, concurrent_op)
            if not client_op:
                # The operation was transformed into a no-op (e.g., inserting into a deleted section).
                raise HTTPException(
                    status_code=409, # Conflict
                    detail=f"Operation could not be applied after transformation. Client revision: {client_revision}, Server revision: {server_revision}"
                )

    # Apply the (potentially transformed) operation.
    document_state["doc"] = apply_operation(document_state["doc"], client_op)
    document_state["revision"] += 1
    history.append(client_op)
    
    return {
        "doc": document_state["doc"],
        "revision": document_state["revision"],
        "applied_op": client_op.to_dict()
    }

@app.post("/reset", tags=["Document"])
def reset_document():
    """
    Resets the document to its original state and revision 0.
    """
    global document_state, history
    document_state = {
        "doc": "Hello, world!",
        "revision": 0
    }
    history = []
    return {"message": "Document reset successfully."}
