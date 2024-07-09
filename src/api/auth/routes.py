__all__ = ["router"]

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from src.schemas.webapp import WebAppInitData
from src.exceptions import NoUserException, UnauthorizedException
from src import repositories as reps
from src import schemas

JWT_SECRET = "somesecret"

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await reps.auth_repository.authenticate(
            int(form_data.username),
            int(form_data.password),
        )

        if not user:
            raise UnauthorizedException()

            token = jwt.encode({"sub": user.id}, JWT_SECRET)
        return schemas.Token(access_token=token)
    except NoUserException:
        pass  # TODO


@router.post("/register")
async def register(initData: WebAppInitData):
    userinfo = await reps.auth_repository.register(initData)

    return userinfo


async def verify(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get('sub')
    except:
        raise UnauthorizedException()


@router.post("/post")
async def post(id = Depends(verify)):
    return f"OK! {id}"
