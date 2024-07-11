__all__ = ["router"]

from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException

from src.middleware.auth_guard import get_id
from src.repositories.user.repository import user_repository
from src.exceptions import Message
from src import repositories as reps
from src import schemas
from src.utils import messages

router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/me",
    responses={
        200: {"model": schemas.UserInfoDTO},
        404: {"model": messages.NotFound},
    },
    response_model_exclude_none=True,
)
async def getUserInfo(id: str = Depends(get_id)):
    return await reps.userinfo_repository.get(id)


@router.put(
    "/me",
    responses={
        200: {"model": schemas.UserInfoDTO},
        404: {"model": messages.NotFound},
    },
    response_model_exclude_none=True,
)
async def updateUserInfo(
    userinfo: schemas.UserInfoDTOUpd,
    id: str = Depends(get_id),
):
    return await reps.userinfo_repository.update(id, userinfo)
