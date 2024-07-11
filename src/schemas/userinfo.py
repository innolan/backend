from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src import schemas


class UserInfoDTOUpd(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None

    about: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None
    metrics: Optional[list[schemas.MetricDTO]] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_user_profile(
        cls,
        user: schemas.UserDTO,
        profile: schemas.ProfileDTO,
    ):
        return UserInfoDTOUpd.model_validate(
            {
                **user.model_dump(exclude={"id"}),
                **profile.model_dump(exclude={"id"}),
            }
        )


class UserInfoDTO(UserInfoDTOUpd):
    id: int = None

    @classmethod
    def from_user_profile(
        cls,
        user: schemas.UserDTO,
        profile: schemas.ProfileDTO,
    ):
        return UserInfoDTO.model_validate(
            {
                **user.model_dump(),
                **profile.model_dump(exclude={"id"}),
            }
        )
