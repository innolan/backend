__all__ = ["SqlAuthRepository", "auth_repository"]


import src.repositories as reps
from src import schemas
from src.repositories.baserepo import SqlBaseRepository
from src.exceptions import NoUserException, UnauthorizedException, EntityExistsException


class SqlAuthRepository(SqlBaseRepository):
    async def authenticate(self, username: int, password: int):
        user = await reps.user_repository.get(username, False)

        if not user:
            raise NoUserException()

        if not user.verify_password(password):
            raise UnauthorizedException()

        return user

    async def register(self, initData: schemas.WebAppInitData):
        if await reps.user_repository.get(initData.user.id):
            raise EntityExistsException()

        userinfo = await reps.userinfo_repository.initialize(initData)

        return userinfo


auth_repository: SqlAuthRepository = SqlAuthRepository()
