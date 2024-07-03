__all__ = ["router"]

from fastapi import APIRouter, Response, status

from src.repositories.user.repository import user_repository

router = APIRouter(prefix="/users")


@router.get("/get/{id}")
async def getUserInfo(id: int, response: Response):
    result = await user_repository.get(id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if result else {}
