from typing import Optional
from pydantic import BaseModel


class MetricDTO(BaseModel):
    id: Optional[int] = None
    name: str
    value: float
    profile_id: Optional[int] = None

    # __hash__ = object.__hash__

    class Config:
        from_attributes = True


# class MetricDTOAdd(MetricDTO):
#     profile_id: int
