__all__ = ["router"]

import os
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from src import schemas
from src import repositories as reps
from src.exceptions import NoUserException, UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token", response_model=schemas.Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await reps.auth_repository.authenticate(
        int(form_data.username),
        int(form_data.password),
    )

    if not user:
        raise UnauthorizedException()

    token = jwt.encode({"sub": user.id}, os.getenv("JWT_TOKEN"))
    return schemas.Token(access_token=token)


@router.post("/register", response_model=schemas.UserInfoDTO)
async def register(initData: schemas.WebAppInitData):
    return await reps.auth_repository.register(initData)

