from typing import Optional
from pydantic import BaseModel


class MetricDTO(BaseModel):
    id: int
    name: str
    value: float

    class Config:
        from_attributes = True
        

class MetricDTOAdd(BaseModel):
    profile_id: int
    name: str
    value: float

    class Config:
        from_attributes = True
