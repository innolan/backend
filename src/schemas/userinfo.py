__all__ = [
    "GetUserInfo",
    "UpdateUserInfo",
]

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProcessedMetric(BaseModel):
    name: str
    value: float


class UserInfo(BaseModel):
    photo_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    about: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    # metrics: Optional[list[ProcessedMetric] | list[None]]           


class GetUserInfo(UserInfo):
    pass


class UpdateUserInfo(GetUserInfo):
    pass
