__all__ = ["SqlAuthRepository", "auth_repository"]

from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.signin import Signin
from src.storage.sql.models import User, Profile
from src.storage.sql.storage import AbstractSQLAlchemyStorage


class SqlAuthRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def signin(self, signin: Signin) -> tuple[User, Profile]:
        async with self._create_session() as session:
            # Look for a user by TG ID
            query = select(User).where(User.tg_id == signin.id)
            user_obj = await session.scalar(query)

            # If the user exists, return
            if user_obj:
                return

            # Otherwise
            profile = Profile()
            session.add(profile)
            session.flush()  # "Soft" save and generate ID

            # Create user
            user = User(
                tg_id=signin.id,
                first_name=signin.first_name,
                last_name=signin.last_name,
                username=signin.username,
                photo_url=signin.photo_url,
                auth_date=signin.auth_date,
                profile_id=profile.id,
            )
            session.add(user)
            await session.commit()

            return (user, profile)


auth_repository: SqlAuthRepository = SqlAuthRepository()
