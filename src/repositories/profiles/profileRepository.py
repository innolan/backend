__all__ = ["SqlProfileRepository", "profile_repository"]

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.signin import CreateProfile
from src.storage.sql.models import Profile
from src.storage.sql.storage import AbstractSQLAlchemyStorage
from typing import Self

from src.storage.sql.models.profile import Profile


class SqlProfileRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, profile: CreateProfile) -> Profile:
        async with self._create_session() as session:
            profile = Profile(**profile.model_dump())
            session.add(profile)
            await session.commit()
            return profile

    async def get(self, id: int) -> Profile | None:
        async with self._create_session() as session:
            profile = await session.get(Profile, id)
            return profile if profile else None

    async def update(self, id: int, profile: CreateProfile) -> Profile | None:
        async with self._create_session() as session:
            profile = await session.get(Profile, id)
            if profile:
                profile = Profile(**profile.model_dump())
                await session.commit()
                return profile

    async def delete(self, id: int) -> Profile | None:
        async with self._create_session() as session:
            profile = await session.get(Profile, id)
            if profile:
                await session.delete(profile)
                await session.commit()
                return profile


profile_repository: SqlProfileRepository = SqlProfileRepository()
