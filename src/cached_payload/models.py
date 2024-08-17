from sqlalchemy import Column, Integer, String, ARRAY
from src.database import Base

class CachedPayload(Base):
    __tablename__ = "cached_payloads"

    id = Column(Integer, primary_key=True, index=True)
    list1 = Column(ARRAY(String), index=True)
    list2 = Column(ARRAY(String), index=True)
    result = Column(String)
