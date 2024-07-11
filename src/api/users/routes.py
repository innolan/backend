__all__ = ["router"]

from fastapi import APIRouter, Depends, HTTPException

from src.middleware.auth_guard import get_id
from src.repositories.user.repository import user_repository
from src.exceptions import Message
from src import repositories as reps
from src import schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserInfoDTO)
async def getUserInfo(id: str = Depends(get_id)):
    return await reps.userinfo_repository.get(id)


@router.post("/me", response_model=schemas.UserInfoDTO)
async def postUserInfo(userinfo: schemas.UserInfoDTO, id: str = Depends(get_id)):
    return await reps.userinfo_repository.update(id, userinfo)
