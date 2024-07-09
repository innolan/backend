import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.exceptions import UnauthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, os.getenv("JWT_TOKEN"), algorithms=["HS256"])
        return payload.get("sub")
    except:
        raise UnauthorizedException()
