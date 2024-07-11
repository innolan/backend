__all__ = ["SqlUserInfoRepository", "userinfo_repository"]

from src.schemas.webapp import WebAppInitData
from src.repositories.baserepo import SqlBaseRepository

from src import schemas
from src import repositories as reps

from src.utils.crypt_context import pwd_context
from src.storage.sql.models import User, Profile
from src.exceptions import EntityNotFoundException, NotImplementedException


class SqlUserInfoRepository(SqlBaseRepository):
    async def initialize(self, initData: WebAppInitData):
        async with self._create_session() as session:
            # 1. Create a user
            user = schemas.UserDTO(
                id=initData.user.id,
                username=initData.user.username,
                first_name=initData.user.first_name,
                last_name=initData.user.last_name,
                auth_date_hash=pwd_context.hash(str(initData.auth_date)),
                photo_url=initData.user.photo_url,
            )
            raw_user = User(**user.model_dump())

            # 2. Create profile
            profile = schemas.ProfileDTO(
                id=initData.user.id,
            )
            raw_profile = Profile(
                user=raw_user,
            )

            # 3. Add them to DB
            session.add(raw_user)
            session.add(raw_profile)
            await session.commit()

            # 4. Return a UserInfo object
            return schemas.UserInfoDTO.from_user_profile(user, profile)

    async def get(self, id: int):
        user = await reps.user_repository.get(id)
        profile = await reps.profile_repository.get(id)

        if not user:
            raise EntityNotFoundException("user")
        if not profile:
            raise EntityNotFoundException("profile")

        return schemas.UserInfoDTO.from_user_profile(user, profile)

    async def update(self, id: int, update: schemas.UserInfoDTO):
        pass

    async def delete(self, id: int):
        # TODO: Fix ordering with cascade deletions. Deleting user should delete profile as well
        await reps.profile_repository.delete(id)
        await reps.user_repository.delete(id)


userinfo_repository: SqlUserInfoRepository = SqlUserInfoRepository()
