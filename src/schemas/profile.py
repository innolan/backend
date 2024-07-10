from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.schemas import MetricDTO


class ProfileDTO(BaseModel):
    id: Optional[int] = None
    about: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    metrics: Optional[list[MetricDTO]] = None

    class Config:
        from_attributes = True
