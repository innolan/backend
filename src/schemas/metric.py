from pydantic import BaseModel


class MetricDTO(BaseModel):
    name: str
    value: float

    class Config:
        from_attributes = True


class MetricDTOUpd(MetricDTO):
    id: int
    name: str
    value: float

    __hash__ = object.__hash__


class MetricDTOAdd(MetricDTO):
    profile_id: int

