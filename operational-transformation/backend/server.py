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

# --- Global State ---
document = "Hello, world!"
history = []


# --- API Endpoints ---

@app.get("/")
async def read_index():
    return FileResponse('../frontend/index.html')

@app.get("/document", tags=["Document"])
def get_document():
    """
    Returns the current state of the document.
    """
    return {"document": document}

@app.post("/apply", tags=["Operations"])
def apply_op(op_model: OperationModel):
    """
    Applies an operation to the document.
    """
    global document, history

    op = Operation(op_model.op_type, op_model.pos, op_model.text or "")

    # In a real system, you would transform this operation against concurrent operations.
    # For this simple example, we'll just apply it directly.
    # To simulate a more realistic scenario, you could transform against the last operation in the history.
    if history:
        last_op = history[-1]
        op = transform(op, last_op)

    if op:
        document = apply_operation(document, op)
        history.append(op)
        return {"document": document}
    else:
        raise HTTPException(
            status_code=400,
            detail="Operation could not be applied."
        )

@app.post("/apply-batch", tags=["Operations"])
def apply_batch(ops: List[OperationModel]):
    """
    Applies a batch of operations to the document, transforming them against each other.
    """
    global document, history

    processed_ops = []
    for op_model in ops:
        op = Operation(op_model.op_type, op_model.pos, op_model.text or "")

        # Transform the incoming operation against all previously processed operations in this batch.
        for processed_op in processed_ops:
            op = transform(op, processed_op)
            if not op:
                # If a transformation results in a None op, we can't continue with this one.
                break
        
        if op:
            document = apply_operation(document, op)
            history.append(op)
            processed_ops.append(op)

    return {"document": document}

@app.post("/reset", tags=["Document"])
def reset_document():
    """
    Resets the document to its original state.
    """
    global document, history
    document = "Hello, world!"
    history = []
    return {"message": "Document reset successfully."}
