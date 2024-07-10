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
                id=initData.user.id,    
            )
            profile = await reps.profile_repository.add(profile_dto)
            await session.commit()

            # 3. Create a UserInfo object
            userinfo = {**user.model_dump(), **profile.model_dump(exclude={"id"})}
            return schemas.UserInfoDTO(**userinfo)

    async def get(self, id: int):
        user = await reps.user_repository.get(id)
        profile = await reps.profile_repository.get(id)

        # Create a UserInfo object
        userinfo = {**user.model_dump(), **profile.model_dump(exclude={"id"})}
        return schemas.UserInfoDTO(**userinfo)

    async def delete(self, id: int):
        await reps.profile_repository.delete(id)
        await reps.user_repository.delete(id)
        


userinfo_repository: SqlUserInfoRepository = SqlUserInfoRepository()
