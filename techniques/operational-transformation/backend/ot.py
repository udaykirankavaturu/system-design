class Operation:
    def __init__(self, op_type, pos, text=""):
        self.op_type = op_type  # "insert" or "delete"
        self.pos = pos
        self.text = text

    def to_dict(self):
        return {"op_type": self.op_type, "pos": self.pos, "text": self.text}

def apply_operation(doc, op):
    if op.op_type == "insert":
        return doc[:op.pos] + op.text + doc[op.pos:]
    elif op.op_type == "delete":
        return doc[:op.pos] + doc[op.pos+len(op.text):]

def transform_insertion_against_insertion(op1, op2):
    """Transforms an insertion operation (op1) against another insertion operation (op2)."""
    # If op1 is before op2, it is not affected.
    if op1.pos < op2.pos:
        return op1
    # If op1 is at or after op2, its position is shifted by the length of op2's insertion.
    else:
        return Operation(op1.op_type, op1.pos + len(op2.text), op1.text)

def transform_insertion_against_deletion(op1, op2):
    """Transforms an insertion operation (op1) against a deletion operation (op2)."""
    # If op1 is before the deleted text, it is not affected.
    if op1.pos <= op2.pos:
        return op1
    # If op1 is after the deleted text, its position is shifted back by the length of the deletion.
    else:
        return Operation(op1.op_type, op1.pos - len(op2.text), op1.text)

def transform_deletion_against_insertion(op1, op2):
    """Transforms a deletion operation (op1) against an insertion operation (op2)."""
    # If the deletion is completely after the insertion, its position is shifted back.
    if op1.pos >= op2.pos + len(op2.text):
        return Operation(op1.op_type, op1.pos - len(op2.text), op1.text)
    # If the deletion is completely before the insertion, it is not affected.
    elif op1.pos + len(op1.text) <= op2.pos:
        return op1
    # If there is an overlap, the behavior is ambiguous. In a real system, this might need more complex logic.
    else: # Overlap
        return None # Deletion is ambiguous, should not happen in a well-behaved client

def transform_deletion_against_deletion(op1, op2):
    """Transforms a deletion operation (op1) against another deletion operation (op2)."""
    # If op1 is before op2, it is not affected.
    if op1.pos < op2.pos:
        return op1
    # If op1 is after op2, its position is shifted back by the length of op2's deletion.
    elif op1.pos > op2.pos:
        return Operation(op1.op_type, op1.pos - len(op2.text), op1.text)
    # If they delete at the same position, they are considered to be deleting the same text.
    else: # Same position
        return None # Both deleting the same text

def transform(op1, op2):
    """Transforms op1 against op2."""
    if op1.op_type == 'insert' and op2.op_type == 'insert':
        return transform_insertion_against_insertion(op1, op2)
    elif op1.op_type == 'insert' and op2.op_type == 'delete':
        return transform_insertion_against_deletion(op1, op2)
    elif op1.op_type == 'delete' and op2.op_type == 'insert':
        return transform_deletion_against_insertion(op1, op2)
    elif op1.op_type == 'delete' and op2.op_type == 'delete':
        return transform_deletion_against_deletion(op1, op2)
