__all__ = ["router"]

import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from src import schemas
from src.utils import messages
from src import repositories as reps
from src.exceptions import UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/token",
    responses={
        200: {"model": schemas.Token},
        401: {"model": messages.Message},
        404: {"model": messages.Message},
    },
)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await reps.auth_repository.authenticate(
        int(form_data.username),
        int(form_data.password),
    )

    if not user:
        raise UnauthorizedException()

    expires_in = datetime.now() + timedelta(minutes=float(os.getenv("JWT_TTL")))
    expires_in = expires_in.timestamp()

    token = jwt.encode({"sub": user.id, 'exp': expires_in}, os.getenv("JWT_TOKEN"))
    return schemas.Token(access_token=token)


@router.post(
    "/register",
    responses={
        200: {"model": schemas.UserInfoDTO},
        409: {"model": messages.Conflict},
    },
)
async def register(initData: schemas.WebAppInitData):
    return await reps.auth_repository.register(initData)
