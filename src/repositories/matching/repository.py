__all__ = ["SqlMatchingRepository", "matching_repository"]


import asyncio
from sqlalchemy import delete, select
from src.repositories.baserepo import SqlBaseRepository

from src.storage.sql.models import Metric, Match
import src.exceptions as exceptions
import src.utils.messages as messages
import src.schemas as schemas
import src.repositories as reps

MINIMUM_MATCHED_METRICS = 3
COMPARE_METRICS_VALUE = 0.3


class SqlMatchingRepository(SqlBaseRepository):
    async def match(self, primary_id: int, secondary_id: int):
        # Ensure that primary and secondary IDs are different
        if primary_id == secondary_id:
            raise exceptions.BadRequestException(
                "Primary ID cannot be equal to secondary ID (selfmatching)"
            )

        # Ensure that the primary id is the largest
        if primary_id > secondary_id:
            primary_id, secondary_id = secondary_id, primary_id

        async with self._create_session() as session:
            # Check that if the match exists and return OK if so
            query = select(Match).where(
                Match.primary_id == primary_id and Match.secondary_id == secondary_id
            )
            existing_match = (await session.execute(query)).scalar_one_or_none()
            if existing_match:
                existing_match.secondary_ack = True
                session.add(existing_match)
                await session.commit()
                return schemas.MatchDTO.model_validate(existing_match)

            # Otherwise, create a match
            raw_match = Match(
                primary_id=primary_id,
                secondary_id=secondary_id,
                primary_ack=True,
                secondary_ack=False,
            )
            session.add(raw_match)

            await session.commit()
            return schemas.MatchDTO.model_validate(raw_match)

    async def delete(self, primary_id: int, secondary_id: int):
        """Delete particular match"""
        async with self._create_session() as session:
            query = delete(Match).where(
                Match.primary_id == primary_id and Match.secondary_id == secondary_id
            )
            await session.execute(query)
            return messages.OK

    async def delete_all(self, primary_id: int):
        """Delete particular all matches for a given ID"""
        async with self._create_session() as session:
            query = delete(Match).where(Match.primary_id == primary_id)
            await session.execute(query)
            return messages.OK

    async def get(self, id) -> list[schemas.ProfileDTO]:
        async with self._create_session() as session:
            query = select(Match).where(
                (Match.primary_id is id and Match.secondary_id is not id)
                or (Match.primary_id is not id and Match.secondary_id is id)
            )
            query = select(Match).where(Match.primary_id == id)
            matches = (await session.execute(query)).scalars().all()

            profiles_promises = []

            for m in matches:
                if m.primary_ack is True and m.secondary_ack is True:
                    if m.primary_id == id:
                        profiles_promises.append(
                            reps.profile_repository.get(m.secondary_id)
                        )
                    else:   
                        profiles_promises.append(
                            reps.profile_repository.get(m.primary_id)
                        )

            profiles = await asyncio.gather(*profiles_promises)
            return profiles


matching_repository = SqlMatchingRepository()
