from pydantic import BaseModel

class CachedPayloadCreate(BaseModel):
    list_1: list[str]
    list_2: list[str]
    result: str
