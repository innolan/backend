__all__ = ["SqlUserRepository", "user_repository"]

from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.userinfo import ProcessedMetric, UserInfo
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
                return
                # raise NoUserException # TODO

            # Get profile
            profile = await session.get(Profile, user.profile_id)
            # TODO
            if not profile:
                return
                # raise NoProfileException # TODO

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


user_repository: SqlUserRepository = SqlUserRepository()
