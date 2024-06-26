__all__ = ["SqlProfileRepository", "profile_repository"]

from src.storage.sql.models import Profile
from src.storage.sql.storage import AbstractSQLAlchemyStorage
from typing import Self, Type

from sqlalchemy import select
from src.storage.sql.models.profile import Profile
from src.schemas.profile import UserProfile

from sqlalchemy.ext.asyncio import AsyncSession

class SqlProfileRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def create(self, profile: UserProfile) -> None:
        async with self._create_session() as session:
            profile = Profile(
                name=profile.name,
                age=profile.age,
                photo=profile.photo,
                date_birth=profile.date_birth,
                sex=profile.sex,
                religion=profile.religion,
                about=profile.about
            )
            session.add(profile)
            await session.commit()

    async def get(self, id: int) -> Profile:
        async with self._create_session() as session:
            profile = await session.get(Profile, id)
            return profile if profile else None


    async def update(self, id: int, profile: UserProfile) -> None:
        async with self._create_session() as session:
            db_profile = await session.get(Profile, id)
            if db_profile:
                db_profile.name = profile.name
                db_profile.age = profile.age
                db_profile.photo = profile.photo
                db_profile.date_birth = profile.date_birth
                db_profile.sex = profile.sex
                db_profile.religion = profile.religion
                db_profile.about = profile.about
                await session.commit()


    async def delete(self, id: int) -> None:
        async with self._create_session() as session:
            profile = await session.get(Profile, id)
            if profile:
                await session.delete(profile)
                await session.commit()



profile_repository: SqlProfileRepository = SqlProfileRepository()

