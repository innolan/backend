# https://core.telegram.org/bots/webapps#webappuser
from typing import Optional

from pydantic import BaseModel, field_validator


# https://core.telegram.org/bots/webapps#webappuser
class WebAppUser(BaseModel):
    id: int
    is_bot: Optional[bool] = None
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    added_to_attachment_menu: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None         

    @field_validator("is_premium", "added_to_attachment_menu", "allows_write_to_pm")
    @classmethod
    def bool_must_be_true(cls, v):
        if v is not None and v is not True:
            raise ValueError("must be True if provided")
        return v


# https://core.telegram.org/bots/webapps#webappinitdata
class WebAppInitData(BaseModel):
    query_id: Optional[str] = None
    user: Optional[WebAppUser] = None
    receiver: Optional[WebAppUser] = None
    chat: Optional[dict] = None
    chat_type: Optional[str] = None
    chat_instance: Optional[str] = None
    start_param: Optional[str] = None
    can_send_after: Optional[int] = None
    auth_date: int
    hash: str
