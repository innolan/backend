__all__ = ["SqlAuthRepository", "auth_repository"]

from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.sql.models.user import User
from src.storage.sql.storage import AbstractSQLAlchemyStorage


class SqlAuthRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()
    
    async def signin(self, t_id: int, username: str):
        async with self._create_session() as session:
            query = select(User).where(User.Tg_id == t_id)
            obj = await session.scalar(query)
            if not obj:
                session.add(User(Tg_id=t_id, User_name=username))
                await session.commit()


auth_repository: SqlAuthRepository = SqlAuthRepository()
