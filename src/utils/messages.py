from pydantic import BaseModel


class Message(BaseModel):
    message: str
    
class OK(Message):
    message: str = "OK!"