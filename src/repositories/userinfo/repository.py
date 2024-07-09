__all__ = ["SqlUserInfoRepository", "userinfo_repository"]

from src.schemas.webapp import WebAppInitData
from src.repositories.baserepo import SqlBaseRepository

from src import schemas
from src import repositories as reps

from src.utils.crypt_context import pwd_context


class SqlUserInfoRepository(SqlBaseRepository):
    async def initialize(self, initData: WebAppInitData):
        async with self._create_session() as session:
            # 1. Create a user
            user_dto = schemas.UserDTO(
                id=initData.user.id,
                username=initData.user.username,
                first_name=initData.user.first_name,
                last_name=initData.user.last_name,
                auth_date_hash=pwd_context.hash(str(initData.auth_date)),
                photo_url=initData.user.photo_url,
            )
            user = await reps.user_repository.add(user_dto)
            await session.commit()

            # 2. Create profile
            profile_dto = schemas.ProfileDTO(
                **initData.user.model_dump(exclude={"id", "metrics"})
            )
            profile_dto.user_id = user.id
            profile = await reps.profile_repository.add(profile_dto)
            await session.commit()

            # 3. Create a UserInfo object
            return {**user.model_dump(), **profile.model_dump(exclude={"id"})}

    async def get(self):
        async with self._create_session() as session:
            user = await reps.user_repository.get(id)
            profile = await reps.profile_repository.get(user)
            await session.commit()

            # Create a UserInfo object
            return {**user.model_dump(), **profile.model_dump(exclude={"id"})}


userinfo_repository: SqlUserInfoRepository = SqlUserInfoRepository()
