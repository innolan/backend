from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src import schemas


class UserInfoDTO(BaseModel):
    id: Optional[int] = None
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
        need_id=True,
    ):
        exclude_list = {} if need_id else {"id"}
        return UserInfoDTO.model_validate(
            {
                **user.model_dump(
                    exclude=exclude_list,
                ),
                **profile.model_dump(
                    exclude={"id"},
                ),
            }
        )
