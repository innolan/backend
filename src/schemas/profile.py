from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.schemas import MetricDTO


class ProfileDTOUpd(BaseModel):
    about: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None

    class Config:
        from_attributes = True
        
class ProfileDTO(ProfileDTOUpd):
    id: int


class ProfileDTORet(ProfileDTOUpd):
    metrics: Optional[list[MetricDTO]] = None