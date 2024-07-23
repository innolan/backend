__all__ = ["SqlMatchingRepository", "matching_repository"]


import asyncio
from sqlalchemy import delete, select
from src.repositories.baserepo import SqlBaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

import src.exceptions as exceptions
from src.storage.sql.models import Match
import src.utils.messages as messages
import src.schemas as schemas
import src.repositories as reps

MINIMUM_MATCHED_METRICS = 3
COMPARE_METRICS_VALUE = 0.3


class SqlMatchingRepository(SqlBaseRepository):
    async def _find_match(
        self,
        primary_id: int,
        secondary_id: int,
        session: AsyncSession,
    ):
        """Look for match with given primary and secondary IDs"""

        # Ensure that the primary id is the largest
        new_primary_id, new_secondary_id = primary_id, secondary_id
        if primary_id < secondary_id:
            new_primary_id, new_secondary_id = secondary_id, primary_id

        query = select(Match).where(
            Match.primary_id == new_primary_id
            and Match.secondary_id == new_secondary_id
        )
        match = (await session.execute(query)).scalar_one_or_none()
        return match

    def _selfmatching_guard(self, primary_id, secondary_id):
        # Ensure that primary and secondary IDs are different
        if primary_id == secondary_id:
            raise exceptions.BadRequestException(
                "Primary ID cannot be equal to secondary ID (selfmatching)"
            )

    async def match(self, matcher: int, matchee: int):
        primary_id, secondary_id = matcher, matchee
        if matcher < matchee:
            primary_id, secondary_id = matchee, matcher

        self._selfmatching_guard(matcher, matchee)

        async with self._create_session() as session:
            # Check that if the match exists
            match = await self._find_match(matcher, matchee, session)
            if match:
                # Set ACK on the correct side
                if matcher == match.primary_id:
                    match.primary_ack = True
                else:
                    match.secondary_ack = True

                session.add(match)
                await session.commit()
                return messages.OK()

            # Create a match if none found
            raw_match = Match(
                primary_id=primary_id if primary_id > secondary_id else secondary_id,
                secondary_id=secondary_id if primary_id > secondary_id else primary_id,
                primary_ack=True if matcher == primary_id else False,
                secondary_ack=True if matcher == secondary_id else False,
            )
            session.add(raw_match)

            await session.commit()
            return messages.OK()

    async def unmatch(self, matcher: int, matchee: int):
        self._selfmatching_guard(matcher, matchee)

        async with self._create_session() as session:
            # Check that if the match exists
            match = await self._find_match(matcher, matchee, session)

            # If match does not exist, return OK early
            if not match:
                return messages.OK()

            # Remove ack if the match exists
            if matcher == match.primary_id:
                match.primary_ack = False
            else:
                match.secondary_ack = False
            session.add(match)

            # Remove match entirely if ACKs are both false
            if match.primary_ack == False and match.secondary_ack == False:
                await session.delete(match)

            await session.commit()
            return messages.OK()

    async def _delete(self, primary_id: int, secondary_id: int):
        """Delete particular match"""
        async with self._create_session() as session:
            query = delete(Match).where(
                Match.primary_id == primary_id and Match.secondary_id == secondary_id
            )
            await session.execute(query)
            return messages.OK()

    async def _delete_all(self, primary_id: int):
        """Delete particular all matches for a given ID"""
        async with self._create_session() as session:
            query = delete(Match).where(Match.primary_id == primary_id)
            await session.execute(query)
            return messages.OK()

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
