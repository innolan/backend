__all__ = ['router']

from fastapi import APIRouter, Depends, Response, status

from src.schemas.signin import Signin
from src.repositories.auth.repository import auth_repository

router = APIRouter(prefix="/auth")


@router.post("/signin")
async def signin(response: Response, signin: Signin = Depends()):
    result = await auth_repository.signin(signin)
    if result:
        user, profile = result
        return (user, profile)
    else: 
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "User already signed in"}
