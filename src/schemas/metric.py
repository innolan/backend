from pydantic import BaseModel


class MetricDTO(BaseModel):
    id: int
    name: str
    value: float
    profile_id: int

    # __hash__ = object.__hash__

    class Config:
        from_attributes = True


# class MetricDTOAdd(MetricDTO):
#     profile_id: int
