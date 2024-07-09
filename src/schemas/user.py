from typing import Optional
from pydantic import BaseModel
from src.utils.crypt_context import pwd_context

class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    auth_date_hash: str
    photo_url: Optional[str] = None

    def verify_password(self, password: int):
        return pwd_context.verify(str(password), str(self.auth_date_hash))

    @classmethod
    def get_password_hash(cls, password):
        return pwd_context.hash(password)

    class Config:
        from_attributes = True
