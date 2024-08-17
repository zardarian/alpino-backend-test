from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.payload import queries, schemas
from src.database import get_db

router = APIRouter()

# External Service Simulation
def transformer_function(list_1: list[str], list_2: list[str]) -> str:
    interleaved = [val for pair in zip(list_1, list_2) for val in pair]
    return ", ".join(interleaved).upper()

@router.post("/payload/", response_model=schemas.PayloadRead)
async def create_payload(payload: schemas.PayloadCreate, db: Session = Depends(get_db)):
    # Transform list_1, list_2 into an interleaved strings
    result = transformer_function(payload.list_1, payload.list_2)

    # Insert into payload
    db_payload = queries.create_payload(db=db, payload_data=payload, result=result)

    return db_payload

@router.get("/payload/{id}", response_model=schemas.PayloadRead)
async def read_payload(id: int, db: Session = Depends(get_db)):
    db_payload = queries.get_payload(db=db, payload_id=id)
    if db_payload is None:
        raise HTTPException(status_code=404, detail="Payload not found")
    return db_payload
