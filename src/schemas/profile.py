from pydantic import BaseModel
from typing import Optional

from src.utils.types import Date
from src.schemas import MetricDTO

class ProfileDTOUpd(BaseModel):
    about: Optional[str] = None
    
    date_of_birth: Optional[
        Date
    ] = None
    sex: Optional[str] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    metrics: Optional[list[MetricDTO]] = None
    likes: Optional[list[int]] = None
    dislikes: Optional[list[int]] = None
    favorites: Optional[list[int]] = None

    class Config:
        from_attributes = True


class ProfileDTORet(ProfileDTOUpd):
    metrics: Optional[list[MetricDTO]] = None


class ProfileDTO(ProfileDTOUpd):
    id: int
    metrics: Optional[list[MetricDTO]] = None
