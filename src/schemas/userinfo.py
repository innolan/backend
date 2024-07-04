# __all__ = [
#     "MetricDTO",
#     "MetricDTOLight",
#     "GetUserInfo",
#     "UpdateUserInfo",
# ]

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MetricDTOUpd(BaseModel):
    id: int
    name: str
    value: float

    class Config:
        from_attributes = True


class MetricDTO(MetricDTOUpd):
    profile_id: int

    class Config:
        from_attributes = True


class MetricDTOAdd(BaseModel):
    profile_id: int
    name: str
    value: float

    class Config:
        from_attributes = True


class ProfileDTOUpd(BaseModel):
    date_of_birth: Optional[datetime] = None
    about: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    about: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    metrics: Optional[list[MetricDTOUpd]] = None

    class Config:
        from_attributes = True


class ProfileDTO(ProfileDTOUpd):
    id: int


class UserDTOUpd(BaseModel):
    # profile_id: Optional[int] = None
    photo_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserDTO(UserDTOUpd):
    id: int

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
    metrics: Optional[list[MetricDTOUpd]] = None


class GetUserInfo(UserInfo):
    pass


class UpdateUserInfo(GetUserInfo):
    pass
