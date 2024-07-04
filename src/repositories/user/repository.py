__all__ = ["user_repository"]


from typing import Self

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories import profile_repository
from src.schemas.userinfo import ProfileDTOUpd, UpdateUserInfo, UserDTOUpd, UserInfo
from src.storage.sql.models import User
from src.storage.sql.storage import AbstractSQLAlchemyStorage
from src.exceptions import NoUserException, NoProfileException


class SqlUserRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def get(self, id: int) -> UserInfo | None:
        async with self._create_session() as session:
            # Get user
            raw_user = await session.get(User, id)
            if not raw_user:
                raise NoUserException()
            user = UserDTOUpd.model_validate(raw_user)
        
            # Get profile
            raw_profile = await profile_repository.get(raw_user.profile_id)
            if not raw_profile:
                raise NoProfileException()
            profile = ProfileDTOUpd.model_validate(raw_profile) 

            # Merge everything into a UserInfo object
            return UserInfo(**(user.model_dump() | profile.model_dump()))

    async def update(self, id: int, update: UpdateUserInfo) -> UserInfo | None:
        async with self._create_session() as session:
            # Get user
            raw_user = await session.get(User, id)
            if not raw_user:
                raise NoUserException()

            # Get profile
            raw_profile = await profile_repository.get(raw_user.profile_id)
            if not raw_profile:
                raise NoProfileException()

            # Update
            raw_user.first_name = update.first_name or raw_user.first_name
            raw_user.last_name = update.last_name or raw_user.last_name
            raw_user.username = update.username or raw_user.username
            raw_user.photo_url = update.photo_url or raw_user.photo_url

            raw_profile.date_of_birth = update.date_of_birth or raw_profile.date_of_birth
            raw_profile.sex = update.sex or raw_profile.sex
            raw_profile.religion = update.religion or raw_profile.religion
            raw_profile.hobby = update.hobby or raw_profile.hobby
            raw_profile.soc_media = update.soc_media or raw_profile.soc_media
            raw_profile.metrics = update.metrics or raw_profile.metrics

            session.add(raw_user)
            await profile_repository.update(id, raw_profile)

            await session.commit()
            
            user = UserDTOUpd.model_validate(raw_user)
            profile = ProfileDTOUpd.model_validate(raw_profile) 

            return UserInfo(**(user.model_dump() | profile.model_dump()))


user_repository: SqlUserRepository = SqlUserRepository()
