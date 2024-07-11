from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class OK(Message):
    detail: str = "OK!"


class Conflict(Message):
    detail: str = "Conflict with an existing entity"


class Unauthorized(Message):
    detail: str = "Unauthorized"


class NotFound(Message):
    detail: str = "Some entity not found"
