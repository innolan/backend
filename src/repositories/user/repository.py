__all__ = ["SqlUserRepository", "user_repository"]

from src.repositories.baserepo import SqlBaseRepository
from src import schemas
from src.storage.sql.models import User


class SqlUserRepository(SqlBaseRepository):
    async def get(self, id: int):
        async with self._create_session() as session:
            raw_user = await session.get(User, id)
            if not raw_user:
                return None
            user = schemas.UserDTO.model_validate(raw_user)
            del user.auth_date_hash
            return user

    async def add(self, user: schemas.UserDTO):
        async with self._create_session() as session:
            raw_user = User(**user.model_dump(exclude={"profile_id"}))
            session.add(raw_user)
            await session.commit()
            return user


user_repository: SqlUserRepository = SqlUserRepository()
