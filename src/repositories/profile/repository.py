__all__ = ["SqlProfileRepository", "profile_repository"]


from deprecated import deprecated
from sqlalchemy import delete, update

from src import schemas
from src.repositories.baserepo import SqlBaseRepository
from src.storage.sql.models import Profile, Metric
from src.exceptions import NotImplementedException
from src.utils.compare_lists import compare_lists
import src.repositories as reps


class SqlProfileRepository(SqlBaseRepository):
    @deprecated("Profile creation is delegated to 'userinfo_repository.initialize()'")
    async def add(self, add: schemas.ProfileDTO):
        raise NotImplementedException()

    # TODO: Rewrite to use less sessions
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

    async def update(self, new_profile: schemas.ProfileDTO):
        async with self._create_session() as session:
            profile = await self.get(new_profile.id)

            # 1. Update regular fields
            profile.about = new_profile.about or profile.about
            profile.date_of_birth = new_profile.date_of_birth or profile.date_of_birth
            profile.sex = new_profile.sex or profile.sex
            profile.religion = new_profile.religion or profile.religion
            profile.hobby = new_profile.hobby or profile.hobby
            profile.soc_media = new_profile.soc_media or profile.soc_media

            session.execute(
                update(Profile)
                .where(Profile.id == profile.id)
                .values(profile.model_dump(exclude={"id", "metric"}))
            )

            # 2. Update metrics
            if new_profile.metrics is not None:
                # Compare metrics
                removed, added, _ = compare_lists(profile.metrics, new_profile.metrics)

                # Delete irrelevant ones
                session.execute(
                    delete(Metric).where(Metric.id.in_(map(lambda m: m.id, removed)))
                )

                # Add relevant ones
                for m in added:
                    metric = Metric(
                        name=m.name,
                        value=m.value,
                        profile_id=profile.id,
                    )
                    session.add(metric)

            await session.commit()

            return await self.get(new_profile.id)

    async def delete(self, id: str):
        async with self._create_session() as session:
            query = delete(Profile).where(Profile.id == id)
            return await session.execute(query)


profile_repository: SqlProfileRepository = SqlProfileRepository()
