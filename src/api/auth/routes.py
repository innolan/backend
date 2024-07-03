__all__ = ["router"]

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.signin import Signin
from src.repositories.auth.repository import auth_repository
from src.exceptions import Message, UserHaveAlreadySignedInMessage

router = APIRouter(prefix="/auth")


@router.get(
    "/signin",
    responses={
        409: {"model": UserHaveAlreadySignedInMessage},
    },
)
async def signin(signin: Signin = Depends()):  # TODO Add return type
    try:
        return await auth_repository.signin(signin)
    except HTTPException as e:
        return Message(e.detail)
