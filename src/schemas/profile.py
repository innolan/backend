from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
