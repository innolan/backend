__all__ = ["router"]

import os
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from src import repositories as reps
from src.schemas import WebAppInitData, Token, UserInfoDTO
from src.exceptions import NoUserException, UnauthorizedException

router = APIRouter(
    prefix="/test",
    tags=["Development routes"],
)


@router.delete("/user")
async def wipe_user(id: str):
    return await reps.userinfo_repository.delete(id)
