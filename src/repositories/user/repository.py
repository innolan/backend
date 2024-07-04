__all__ = ["SqlUserRepository", "user_repository"]


from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NoUserException, NoProfileException
from src.schemas.userinfo import UpdateUserInfo, UserInfo
from src.storage.sql.models import User, Profile, Metric
from src.storage.sql.storage import AbstractSQLAlchemyStorage


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
            user = await session.get(User, id)
            if not user:
                raise NoUserException()

            # Get profile
            profile = await session.get(Profile, user.profile_id)
            if not profile:
                raise NoProfileException()

            # Aggregate all metrics (really fucking bad)
            query = select(Metric).where(Metric.profile_id == profile.id)
            # metrics = list(
            #     map(
            #         lambda m: ProcessedMetric(
            #             name=m.name,
            #             value=float(m.value - 50) / 100,
            #         ),
            #         (await session.execute(query)).scalars().all(),
            #     )
            # )

            # Merge everything into a UserInfo object
            return UserInfo(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                photo_url=user.photo_url,
                about=profile.about,
                date_of_birth=profile.date_of_birth,
                sex=profile.sex,
                religion=profile.religion,
                hobby=profile.hobby,
                soc_media=profile.soc_media,
                # metrics=metrics,
            )

    async def update(self, id: int, update: UpdateUserInfo) -> UserInfo | None:
        async with self._create_session() as session:
            # Get user
            user = await session.get(User, id)
            if not user:
                raise NoUserException()

            # Get profile
            profile = await session.get(Profile, user.profile_id)
            if not profile:
                raise NoProfileException()

            # Update
            # metrics = update.metrics | profile.metrics
            user.first_name = update.first_name or user.first_name
            user.last_name = update.last_name or user.last_name
            user.username = update.username or user.username
            user.photo_url = update.photo_url or user.photo_url

            profile.date_of_birth = update.date_of_birth or profile.date_of_birth
            profile.sex = update.sex or profile.sex
            profile.religion = update.religion or profile.religion
            profile.hobby = update.hobby or profile.hobby
            profile.soc_media = update.soc_media or profile.soc_media

            session.add(user)
            session.add(profile)

            await session.commit()

            return UserInfo(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                photo_url=user.photo_url,
                about=profile.about,
                date_of_birth=profile.date_of_birth,
                sex=profile.sex,
                religion=profile.religion,
                hobby=profile.hobby,
                soc_media=profile.soc_media,
                # metrics=metrics,
            )


user_repository: SqlUserRepository = SqlUserRepository()
