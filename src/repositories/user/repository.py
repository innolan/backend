__all__ = ["SqlUserRepository", "user_repository"]

from sqlalchemy import delete, update
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

    @deprecated("User creation is delegated to 'userinfo_repository.initialize()'")
    async def add(self, user: schemas.UserDTO):
        raise NotImplementedException()

    async def update(self, id: int, new_user: schemas.UserDTO):
        user = await self.get(id)

        user.id = new_user.id or user.id
        user.first_name = new_user.first_name or user.first_name
        user.last_name = new_user.last_name or user.last_name
        user.username = new_user.username or user.username
        user.photo_url = new_user.photo_url or user.photo_url

        async with self._create_session() as session:
            await session.execute(
                update(User)
                .where(User.id == id)
                .values(**user.model_dump(exclude={"id"}))
            )
            await session.commit()
            return new_user

    async def delete(self, id: int):
        async with self._create_session() as session:
            query = delete(User).where(User.id == id)
            await session.execute(query)
            await session.commit()


user_repository: SqlUserRepository = SqlUserRepository()
