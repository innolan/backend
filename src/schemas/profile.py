from pydantic import BaseModel, StringConstraints, constr
from datetime import datetime
from typing import Annotated, Optional

from src.schemas import MetricDTO


class ProfileDTOUpd(BaseModel):
    about: Optional[str] = None
    date_of_birth: Optional[
        Annotated[
            str,
            StringConstraints(
                pattern=r"^(((0[1-9]|[12][0-9]|3[01])[- /.](0[13578]|1[02])|(0[1-9]|[12][0-9]|30)[- /.](0[469]|11)|(0[1-9]|1\d|2[0-8])[- /.]02)[- /.]\d{4}|29[- /.]02[- /.](\d{2}(0[48]|[2468][048]|[13579][26])|([02468][048]|[1359][26])00))$"
            ),
        ]
    ] = None
    sex: Optional[int] = None
    religion: Optional[str] = None
    hobby: Optional[list[str]] = None
    soc_media: Optional[list[str]] = None

    class Config:
        from_attributes = True


class ProfileDTORet(ProfileDTOUpd):
    metrics: Optional[list[MetricDTO]] = None


class ProfileDTO(ProfileDTOUpd):
    id: int
    metrics: Optional[list[MetricDTO]] = None
