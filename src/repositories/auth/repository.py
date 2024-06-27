__all__ = ["SqlAuthRepository", "auth_repository"]

from typing import Self

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.signin import CreateProfile, Signin
from src.storage.sql.models import User, Profile
from src.storage.sql.storage import AbstractSQLAlchemyStorage


class SqlAuthRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def signin(self, signin: Signin):
        async with self._create_session() as session:
            query = select(User).where(User.tg_id == signin.tg_id)
            user_obj = await session.scalar(query)

            if not user_obj:
                profile = Profile(
                    **CreateProfile(
                        first_name=signin.first_name,
                        last_name=signin.last_name,
                        username=signin.username,
                        photo_url=signin.photo_url,
                    ).model_dump()
                )
                session.add(profile)
                await session.commit()
                
                session.add(
                    User(
                        tg_id=signin.tg_id,
                        profile_id=profile.id,
                    )
                )
                await session.commit()


auth_repository: SqlAuthRepository = SqlAuthRepository()
