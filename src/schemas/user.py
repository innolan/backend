from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    auth_date: int
    photo_url: Optional[str] = None

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.auth_date)

    @classmethod
    def get_password_hash(cls, password):
        return pwd_context.hash(password)
    
    class Config:
            from_attributes = True
