from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.schemas.metric import MetricDTOUpd


class ProfileDTO(BaseModel):
    id: int
    about: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    metrics: Optional[list[MetricDTOUpd]]

    class Config:
        from_attributes = True
