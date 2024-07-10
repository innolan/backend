__all__ = ["SqlUserRepository", "user_repository"]

from sqlalchemy import delete
from src.repositories.baserepo import SqlBaseRepository
from src import schemas
from src.storage.sql.models import User


class SqlUserRepository(SqlBaseRepository):
    async def get(self, id: int, remove_hash = True):
        async with self._create_session() as session:
            raw_user = await session.get(User, id)
            if not raw_user:
                return None
            user = schemas.UserDTO.model_validate(raw_user)
            if remove_hash:
                del user.auth_date_hash
            return user

    async def add(self, user: schemas.UserDTO):
        async with self._create_session() as session:
            raw_user = User(**user.model_dump(exclude={"profile_id"}))
            session.add(raw_user)
            await session.commit()
            return user
        
    async def delete(self, id: int):
        async with self._create_session() as session:
            query = delete(User).where(User.id == id)
            return await session.scalar(query)


user_repository: SqlUserRepository = SqlUserRepository()
