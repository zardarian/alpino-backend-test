from sqlalchemy.orm import Session
from src.payload import models, schemas

def create_payload(db: Session, payload_data: schemas.PayloadCreate, result: str):
    db_payload = models.Payload(data=str(payload_data.dict()), result=result)
    db.add(db_payload)
    db.commit()
    db.refresh(db_payload)
    return db_payload

def get_payload(db: Session, payload_id: int):
    return db.query(models.Payload).filter(models.Payload.id == payload_id).first()
