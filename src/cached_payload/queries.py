from sqlalchemy.orm import Session
from src.cached_payload import models, schemas

def create_cached_payload(db: Session, cached_payload_data: schemas.CachedPayloadCreate):
    db_payload = models.CachedPayload(list1=cached_payload_data.list_1, list2=cached_payload_data.list_2, result=cached_payload_data.result)
    db.add(db_payload)
    db.commit()
    db.refresh(db_payload)
    return db_payload

def get_cached_payload_by_list1_list2(db: Session, list1: list[str], list2: list[str]):
    return db.query(models.CachedPayload).filter(models.CachedPayload.list1 == list1, models.CachedPayload.list2 == list2).first()
