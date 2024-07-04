__all__ = ["SqlProfileRepository", "profile_repository"]


from typing import Self

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.userinfo import MetricDTO, ProfileDTO, ProfileDTOUpd
from src.storage.sql.models import Profile, Metric
from src.storage.sql.storage import AbstractSQLAlchemyStorage
from src.exceptions import NoProfileException
from src.utils.compare_lists import compare_lists
import src.repositories as reps

class SqlProfileRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def get(self, profile_id: int) -> ProfileDTO | None:
        async with self._create_session() as session:
            # Get profile
            profile = await session.get(Profile, profile_id)
            if not profile:
                raise NoProfileException()
            # Get metrics
            metrics = await reps.metric_repository.get_by_profile_id(profile_id)
            # Validate profile and add metrics            
            profile_dto = ProfileDTOUpd.model_validate(profile)
            profile_dto.metrics = metrics
            
            return profile_dto

    async def is_profile_exist(self, profile_id):
        async with self._create_session() as session:
            # Get profile
            profile = await session.get(Profile, profile_id)
            return True if profile else False

    async def update(self, id: int, update: ProfileDTO) -> ProfileDTO | None:
        async with self._create_session() as session:
            # Get profile
            profile = await self.get(id)

            # old_metrics = reps.metric_repository.``
            profile.date_of_birth = update.date_of_birth or profile.date_of_birth
            profile.sex = update.sex or profile.sex
            profile.religion = update.religion or profile.religion
            profile.hobby = update.hobby or profile.hobby
            profile.soc_media = update.soc_media or profile.soc_media

            # Special case for metrics

            # Compare metrics
            removed, added, _ = compare_lists(profile.metrics, profile.metrics)

            # Delete irrelevant ones
            session.execute(
                delete(Metric).where(Metric.id.in_([m.id for m in removed]))
            )
            # Add relevant ones
            session.execute(
                insert(Metric),
                [MetricDTO.model_construct(m.model_dump()) for m in added],
            )

            await session.commit()

            return await self.get(id)


profile_repository: SqlProfileRepository = SqlProfileRepository()
