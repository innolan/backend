__all__ = ["SqlMetricRepository", "metric_repository"]


from sqlalchemy import select
from src.repositories.baserepo import SqlBaseRepository

from src import schemas
from src import repositories as reps
from src.exceptions import NoMetricException, NoProfileException
from src.storage.sql.models import Metric


class SqlMetricRepository(SqlBaseRepository):

    async def get(self, id: int):
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            if not metric:
                raise NoMetricException()

            return schemas.MetricDTO.model_validate(metric)

    async def create(self, create: schemas.MetricDTO):
        async with self._create_session() as session:
            metric = Metric(**create.model_dump(exclude={"id"}))
            session.add(metric)
            await session.commit()

            return await self.get(metric.id)

    async def get_by_profile_id(self, profile_id: int):
        async with self._create_session() as session:
            if not (await reps.profile_repository.is_profile_exist(profile_id)):
                raise NoProfileException()

            query = select(Metric).where(Metric.profile_id == profile_id)
            scalars = (await session.execute(query)).scalars().all()
            metrics = [schemas.MetricDTO.model_validate(s) for s in scalars]
            return metrics

    async def update(self, update: schemas.MetricDTO):
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            if not metric:
                raise NoMetricException()

            # Update relevant values
            metric.name = update.name or metric.name
            metric.value = update.value or metric.value

            session.add(metric)
            await session.commit()

            return await self.get(id)


metric_repository: SqlMetricRepository = SqlMetricRepository()
