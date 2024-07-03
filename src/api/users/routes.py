__all__ = ["router"]

from fastapi import APIRouter, Response, status

from src.repositories.user.repository import user_repository
from src.schemas.userinfo import UpdateUserInfo, UserInfo

router = APIRouter(prefix="/users")


@router.get("/get/{id}")
async def getUserInfo(id: int, response: Response) -> UserInfo | None:
    result = await user_repository.get(id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if result else {}

@router.get("/update/{id}")
async def getUserInfo(id: int, update: UpdateUserInfo) -> UserInfo | None:
    result = await user_repository.update(id, update)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if result else {}
