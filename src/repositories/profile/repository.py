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
            profile = schemas.ProfileDTORet.model_validate(raw_profile)

            metrics = await reps.metric_repository.get_by_profile_id(id)
            profile.metrics = metrics

            return profile

    async def is_profile_exist(self, profile_id):
        async with self._create_session() as session:
            profile = await session.get(Profile, profile_id)
            return True if profile else False

    async def update(self, id: int, new_profile: schemas.ProfileDTOUpd):
        async with self._create_session() as session:
            profile_ret = await self.get(id)

            profile_ret.about = new_profile.about or profile_ret.about
            profile_ret.date_of_birth = new_profile.date_of_birth or profile_ret.date_of_birth
            profile_ret.sex = new_profile.sex or profile_ret.sex
            profile_ret.religion = new_profile.religion or profile_ret.religion
            profile_ret.hobby = new_profile.hobby or profile_ret.hobby
            profile_ret.soc_media = new_profile.soc_media or profile_ret.soc_media

            await session.execute(
                update(Profile)
                .where(Profile.id == id)
                .values(**profile_ret.model_dump(exclude={"metrics"}))
            )

            await session.commit()

            return await self.get(id)

    async def delete(self, id: int):
        async with self._create_session() as session:
            query = delete(Profile).where(Profile.id == id)
            await session.execute(query)
            await session.commit()


profile_repository: SqlProfileRepository = SqlProfileRepository()
