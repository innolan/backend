__all__ = ["Signin"]

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Signin(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    # photo_url: str
    auth_date: datetime
    # hash: str
