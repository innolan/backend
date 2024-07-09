__all__ = ["router"]

import os
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from src import repositories as reps
from src import schemas
from src.middleware.auth_guard import get_id
from src.schemas.webapp import WebAppInitData
from src.exceptions import NoUserException, UnauthorizedException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await reps.auth_repository.authenticate(
            int(form_data.username),
            int(form_data.password),
        )

        if not user:
            raise UnauthorizedException()

        token = jwt.encode({"sub": user.id}, os.getenv("JWT_TOKEN"))
        return schemas.Token(access_token=token)
    except NoUserException:
        pass  # TODO


@router.post("/register")
async def register(initData: WebAppInitData):
    userinfo = await reps.auth_repository.register(initData)

    return userinfo


@router.post("/post")
async def post(id=Depends(get_id)):
    return f"OK! {id}"
