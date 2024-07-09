__all__ = ["router"]

from fastapi import APIRouter, Depends, HTTPException

from src.middleware.auth_guard import get_id
from src.repositories.user.repository import user_repository
from src.exceptions import Message
from src import repositories as reps

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def getUserInfo(id: str = Depends(get_id)):
    return await reps.user_repository.get(id)

