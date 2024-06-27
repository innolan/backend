from fastapi import APIRouter, Depends

from src.schemas.signin import Signin
from src.repositories.auth.repository import auth_repository

router = APIRouter(prefix="/auth")


@router.post("/signin")
async def signin(signin: Signin = Depends()):
    created = await auth_repository.signin(signin)
