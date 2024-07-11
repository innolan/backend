__all__ = ["router"]

from fastapi import APIRouter

from src import repositories as reps
from src.utils import messages

router = APIRouter(
    prefix="/test",
    tags=["Development routes"],
)


@router.delete("/user", response_model=messages.OK)
async def wipe_user(id: int):
    await reps.userinfo_repository.delete(id)
    return messages.OK()
