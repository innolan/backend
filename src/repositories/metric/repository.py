__all__ = ["SqlMetricRepository", "metric_repository"]


from sqlalchemy import select, update
from src.repositories.baserepo import SqlBaseRepository

from src import schemas
from src import repositories as reps
from src.exceptions import EntityNotFoundException, NoMetricException, NotImplementedException
from src.storage.sql.models import Metric


class SqlMetricRepository(SqlBaseRepository):
    async def get(self, id: int):
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            if not metric:
                return None

            return schemas.MetricDTO.model_validate(metric)

    async def create(self, profile_id: int, create: schemas.MetricDTOAdd):
        async with self._create_session() as session:
            metric = Metric(
                **{
                    **create.model_dump(include={"name", "value"}),
                    **{"profile_id": profile_id},
                }
            )
            session.add(metric)
            await session.commit()

            return await self.get(metric.id)

    async def delete(self, id):
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            session.delete(metric)
            if not metric:
                raise NoMetricException()
            await session.commit()

    async def get_by_profile_id(self, profile_id: int):
        # TODO: Reconsider method
        # raise NotImplementedException()
        async with self._create_session() as session:
            if not (await reps.profile_repository.is_profile_exist(profile_id)):
                raise EntityNotFoundException('profile')

            query = select(Metric).where(Metric.profile_id == profile_id)
            scalars = (await session.execute(query)).scalars().all()
            metrics = [schemas.MetricDTO.model_validate(s) for s in scalars]
            # Strip metrics of profile_id
            metrics = list(
                map(
                    lambda m: schemas.MetricDTO(**m.model_dump(exclude={"profile_id"})),
                    metrics,
                )
            )
            return metrics

    async def update(self, profile_id: int, new_metric: schemas.MetricDTO):
        async with self._create_session() as session:
            metric = await session.get(Metric, id)
            if not metric:
                raise NoMetricException()

            # Update relevant values
            metric.name = new_metric.name or metric.name
            metric.value = new_metric.value or metric.value

            await session.execute(
                update(Metric)
                .where(Metric.id == id)
                .values(**new_metric.model_dump(include={"name", "value"}))
            )
            await session.commit()

            return await self.get(id)


metric_repository: SqlMetricRepository = SqlMetricRepository()
