from sqlalchemy import Column, Integer, String
from src.database import Base

class Payload(Base):
    __tablename__ = "payloads"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, index=True)
    result = Column(String)
