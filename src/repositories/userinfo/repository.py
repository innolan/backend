__all__ = ["SqlUserInfoRepository", "userinfo_repository"]

from src.schemas.webapp import WebAppInitData
from src.repositories.baserepo import SqlBaseRepository

from src import schemas
from src import repositories as reps

from src.utils.crypt_context import pwd_context
from src.storage.sql.models import User, Profile
from src.exceptions import EntityNotFoundException, NotImplementedException

from sqlalchemy import delete, update


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
                photo_url=[initData.user.photo_url] if initData.user.photo_url is not None else None,
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

    async def update(self, id: int, update: schemas.UserInfoDTOUpd):
        userinfo = await self.get(id)
        
        userinfo.first_name = update.first_name or userinfo.first_name
        userinfo.last_name = update.last_name or userinfo.last_name
        userinfo.username = update.username or userinfo.username
        userinfo.photo_url = update.photo_url or userinfo.photo_url

        userinfo.about = update.about or userinfo.about
        userinfo.date_of_birth = update.date_of_birth or userinfo.date_of_birth
        userinfo.sex = update.sex or userinfo.sex
        userinfo.religion = update.religion or userinfo.religion
        userinfo.hobby = update.hobby or userinfo.hobby
        userinfo.soc_media = update.soc_media or userinfo.soc_media
        userinfo.metrics = update.metrics or userinfo.metrics
        
        await reps.user_repository.update(id, schemas.UserDTO.model_validate(userinfo))
        await reps.profile_repository.update(id, schemas.ProfileDTOUpd.model_validate(userinfo))
        
        return await self.get(id)

    async def delete(self, id: int):
        # TODO: Fix ordering with cascade deletions. Deleting user should delete profile as well
        await reps.profile_repository.delete(id)
        await reps.user_repository.delete(id)

    # Functions for likes, dislikes and favourites
    async def putLike(self, target_id, id):
        async with self._create_session() as session:
            user = await reps.user_repository.get(id)
            profile = await reps.profile_repository.get(id)
            if not user:
                raise EntityNotFoundException("user")
            if not profile:
                raise EntityNotFoundException("profile")

            profile.likes.append(target_id)
            await session.execute(
                update(Profile)
                .where(Profile.id == profile.id)
                .values(profile.model_dump(exclude={"id", "metric"}))
            )
            await session.commit()

            return await self.get(id)


    async def putDislike(self, target_id, id):
        async with self._create_session() as session:
            user = await reps.user_repository.get(id)
            profile = await reps.profile_repository.get(id)
            if not user:
                raise EntityNotFoundException("user")
            if not profile:
                raise EntityNotFoundException("profile")

            profile.dislikes.append(target_id)
            await session.execute(
                update(Profile)
                .where(Profile.id == profile.id)
                .values(profile.model_dump(exclude={"id", "metric"}))
            )
            await session.commit()

            return (await self.get(id)).dislikes


    async def putFavorite(self, target_id, id):
        async with self._create_session() as session:
            user = await reps.user_repository.get(id)
            profile = await reps.profile_repository.get(id)
            if not user:
                raise EntityNotFoundException("user")
            if not profile:
                raise EntityNotFoundException("profile")

            profile.favorites.append(target_id)
            await session.execute(
                update(Profile)
                .where(Profile.id == profile.id)
                .values(profile.model_dump(exclude={"id", "metric"}))
            )
            await session.commit()

            return (await self.get(id)).favorites



userinfo_repository: SqlUserInfoRepository = SqlUserInfoRepository()
