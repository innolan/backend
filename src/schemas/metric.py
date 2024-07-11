from typing import Optional
from pydantic import BaseModel


class MetricDTO(BaseModel):
    name: str
    value: float

    class Config:
        from_attributes = True


class MetricDTOAdd(MetricDTO):
    profile_id: Optional[int] = None

class MetricDTOUpd(MetricDTO):
    id: int 
