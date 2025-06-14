from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    quantity: Optional[int] = None
    note: Optional[str] = None
    category: Optional[str] = None
    purchased: bool = False

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

    @validator('created_at', 'updated_at', pre=True)
    def datetime_to_str(cls, v):
        return v.isoformat() if isinstance(v, datetime) else v
