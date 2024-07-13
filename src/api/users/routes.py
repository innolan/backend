__all__ = ["router"]

from fastapi import APIRouter, Depends

from src import schemas
from src import repositories as reps
from src.utils import messages
from src.middleware.auth_guard import get_id

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
async def updateUserInfo(userinfo: schemas.UserInfoDTOUpd, id: str = Depends(get_id)):
    return await reps.userinfo_repository.update(id, userinfo)


@router.put(
    "/me/likes/{target_id}",
    responses={
        200: {"model": list[int]},
        404: {"model": messages.NotFound},
    },
)
async def putLikes(target_id: int, id: str = Depends(get_id)):
    return await reps.userinfo_repository.putLike(target_id, id)


@router.put(
    "/me/dislikes/{target_id}",
    responses={
        200: {"model": list[int]},
        404: {"model": messages.NotFound},
    },
)
async def putDislikes(target_id: int, id: str = Depends(get_id)):
    return await reps.userinfo_repository.putDislike(target_id, id)


@router.put(
    "/me/favorites/{target_id}",
    responses={
        200: {"model": list[int]},
        404: {"model": messages.NotFound},
    },
)
async def putFavorites(target_id: int, id: str = Depends(get_id)):
    return await reps.userinfo_repository.putFavorite(target_id, id)
