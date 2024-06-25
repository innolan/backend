from fastapi import APIRouter

from src.repositories.auth.repository import auth_repository

router = APIRouter(prefix="/auth")


@router.post("/signin")
async def signin(
    t_id: int,
    username: str,
):
    created = await auth_repository.signin(t_id, username)
