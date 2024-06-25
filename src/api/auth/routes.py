from fastapi import APIRouter
from pydantic import BaseModel

from src.repositories.auth.repository import auth_repository

router = APIRouter(prefix="/auth")


class Signin(BaseModel):
    t_id: int
    username: str


@router.post("/signin")
async def signin(signin: Signin):
    created = await auth_repository.signin(**signin.model_dump())
