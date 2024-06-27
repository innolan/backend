__all__ = ["CreateProfile"]

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Signin(BaseModel):
    tg_id: int
    first_name: str
    last_name: Optional[str] = None
    username: str
    photo_url: str
    auth_date: datetime
    # hash: str # TODO Once the domain is up, switch to LoginUrl pipeline


class CreateProfile(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    username: str
    photo_url: str
    date_of_birth: Optional[datetime] = None
    sex: Optional[str] = None
    religion: Optional[str] = None
    about: Optional[str] = None
