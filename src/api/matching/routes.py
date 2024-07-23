__all__ = ["router"]

from fastapi import APIRouter, Depends

from src.middleware.auth_guard import get_id
from src import repositories as reps
from src.utils import messages
import src.schemas as schemas

router = APIRouter(
    prefix="/matching",
    tags=["Matching routes"],
)


@router.get("/get")
async def get_match(id: str = Depends(get_id)):
    await reps.matching_repository.get(id)


@router.put(
    "/match/{secondary_id}",
    responses={
        200: {"model": schemas.MatchDTO},
        401: {"model": messages.Message},
    },
)
async def get_match(secondary_id: int, primary_id: int = Depends(get_id)):
    return await reps.matching_repository.match(primary_id, secondary_id)
