__all__ = ["SqlMetricRepository", "metric_repository"]


from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.storage.sql.storage import AbstractSQLAlchemyStorage

from src.schemas.userinfo import (
    MetricDTO,
    MetricDTOAdd,
    MetricDTOUpd,
)
from src.exceptions import NoMetricException, NoProfileException
from src.storage.sql.models import Metric
import src.repositories as reps


class SqlMetricRepository:
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()

    async def get(self, id: int) -> MetricDTO | None:
        async with self._create_session() as session:
            # Get metric
            metric = await session.get(Metric, id)
            if not metric:
                raise NoMetricException()

            return MetricDTO.model_validate(metric)

    async def get_by_profile_id(self, profile_id: int) -> list[MetricDTOUpd] | None:
        async with self._create_session() as session:
            # Will throw if no profile found
            if not (await reps.profile_repository.is_profile_exist(profile_id)):
                 raise NoProfileException()

            # Form query
            query = select(Metric).where(Metric.profile_id == profile_id)
            # Get scalars
            scalars = (await session.execute(query)).scalars().all()
            # Validate DTOs
            metrics = [MetricDTOUpd.model_validate(s) for s in scalars]
            return metrics

    async def create(self, create: MetricDTOAdd) -> MetricDTO | None:
        """Add metric

        Args:
            create (MetricDTOAdd): Metric "ADD" DTO

        Returns:
            MetricDTO | None: Newly created metric
        """
        async with self._create_session() as session:
            metric = Metric(**create.model_dump())
            session.add(metric)
            await session.commit()

            return await self.get(metric.id)

    async def update(self, id: int, update: MetricDTOUpd) -> MetricDTO | None:
        """Update metric

        Args:
            id (int):  ID of metric
            update (MetricDTO): Update DTO

        Returns:
            MetricDTO | None: Fresh metric

        Raises:
            NoMetricException: Raised if no metric was found
        """
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            if not metric:
                raise NoMetricException()

            # Update relevant values
            metric.name = update.name or metric.name
            metric.value = update.value or metric.value

            return await self.get(id)


metric_repository: SqlMetricRepository = SqlMetricRepository()
