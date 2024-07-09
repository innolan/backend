__all__ = ["SqlProfileRepository", "profile_repository"]


from asyncio import gather
from sqlalchemy import delete, insert, select

from src import schemas
from src.repositories.baserepo import SqlBaseRepository
from src.storage.sql.models import Profile, Metric
from src.exceptions import EntityExistsException, NoProfileException
from src.utils.compare_lists import compare_lists
import src.repositories as reps


class SqlProfileRepository(SqlBaseRepository):
    async def add(self, create: schemas.ProfileDTO):
        async with self._create_session() as session:
            raw_profile = Profile(**create.model_dump(exclude={"metrics"}))
            session.add(raw_profile)
            await session.commit()

        
            metrics: list[schemas.MetricDTO] = None
            if create.metrics is not None:
                # Write all metrics
                metrics = await gather(
                    *[
                        reps.metric_repository.create(
                            schemas.MetricDTO(
                                name=m.name,
                                value=m.value,
                                profile_id=raw_profile.id,
                            )
                        )
                        for m in create.metrics
                    ]
                )
                # Strip metrics of profile_id
                metrics = list(
                    map(
                        lambda m: schemas.MetricDTO(**m.model_dump(exclude={"profile_id"})),
                        metrics,
                    )
                )
                

            await session.commit()
            profile_dto = schemas.ProfileDTO.model_validate(raw_profile)
            
            profile_dto.metrics = metrics
            return profile_dto

    async def get(self, id: int):
        async with self._create_session() as session:
            raw_profile = await session.get(Profile, id)
            if not raw_profile:
                return None
            profile = schemas.ProfileDTO.model_validate(raw_profile)

            metrics = await reps.metric_repository.get_by_profile_id(id)
            profile.metrics = metrics

            return profile

    async def is_profile_exist(self, profile_id):
        async with self._create_session() as session:
            profile = await session.get(Profile, profile_id)
            return True if profile else False

    async def update(self, update: schemas.ProfileDTO):
        async with self._create_session() as session:
            profile = await self.get(update.id)

            # Compare metrics
            removed, added, _ = compare_lists(profile.metrics, update.metrics)

            # Delete irrelevant ones
            await gather([reps.metric_repository.delete(m.id) for m in removed])

            # Add relevant ones
            await gather(
                [
                    reps.metric_repository.create(
                        schemas.MetricDTO(
                            name=m.name,
                            value=m.value,
                            profile_id=profile.id,
                        )
                    )
                    for m in added
                ]
            )

            await session.commit()

            return await self.get(update.id)


profile_repository: SqlProfileRepository = SqlProfileRepository()
