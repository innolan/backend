__all__ = ["SqlUserRepository", "user_repository"]

from sqlalchemy import delete
from deprecated import deprecated

from src import schemas
from src.storage.sql.models import User
from src.exceptions import NotImplementedException
from src.repositories.baserepo import SqlBaseRepository

class SqlUserRepository(SqlBaseRepository):
    async def get(self, id: int, remove_hash=True):
        async with self._create_session() as session:
            raw_user = await session.get(User, id)
            if not raw_user:
                return None
            user = schemas.UserDTO.model_validate(raw_user)
            if remove_hash:
                del user.auth_date_hash
            return user

    @deprecated("No business logic requires this level of fine-tuning for user creation")
    async def add(self, user: schemas.UserDTO):
        raise NotImplementedException()

    async def update(self, id: int, update: schemas.UserDTO):
        # TODO
        raise NotImplementedException()

    async def delete(self, id: int):
        async with self._create_session() as session:
            query = delete(User).where(User.id == id)
            return await session.scalar(query)


user_repository: SqlUserRepository = SqlUserRepository()
