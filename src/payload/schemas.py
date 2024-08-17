from pydantic import BaseModel

class PayloadCreate(BaseModel):
    list_1: list[str]
    list_2: list[str]

class PayloadRead(BaseModel):
    id: int
    result: str

    class Config:
        orm_mode = True
