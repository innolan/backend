__all__ = ["router"]

from fastapi import APIRouter, HTTPException, Response, status

from src.repositories.user.repository import user_repository
from src.schemas.userinfo import UpdateUserInfo, UserInfo
from src.exceptions import Message, ProfileNotFoundMessage, UserNotFoundMessage

router = APIRouter(prefix="/users")


@router.get(
    "/get/{id}",
    responses={
        404: {
            "model": Message,
        },
    },
)
async def getUserInfo(id: int, response: Response) -> UserInfo | None:
    try:
        return await user_repository.get(id)
    except HTTPException as e:
        return Message(e.detail)


@router.post(
    "/update/{id}",
    responses={
        404: {"model": Message},
    },
)
async def getUserInfo(
    id: int, update: UpdateUserInfo, response: Response
) -> UserInfo | None:
    try:
        return await user_repository.update(id, update)
    except HTTPException as e: 
        return Message(e)
        
