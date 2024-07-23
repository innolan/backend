__all__ = ["SqlMatchingRepository", "matching_repository"]


from sqlalchemy import delete, select
from src.repositories.baserepo import SqlBaseRepository

from src.exceptions import (
    EntityNotFoundException,
    NoMetricException,
    NotImplementedException,
)
from src.storage.sql.models import Metric, Match
import src.utils.messages as messages
import src.schemas as schemas

MINIMUM_MATCHED_METRICS = 3
COMPARE_METRICS_VALUE = 0.3


class SqlMatchingRepository(SqlBaseRepository):
    async def match(self, primary_id: int, secondary_id: int):
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
                return schemas.MatchDTO.model_validate(existing_match)

            # Otherwise, create a match
            raw_match = Match(
                primary_id=primary_id,
                secondary_id=secondary_id,
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

    def compare_metrics(self, firstMetric: Metric, secondMetric: Metric) -> bool:
        if abs(firstMetric.value - secondMetric.value) > COMPARE_METRICS_VALUE:
            return False
        return True

    def compare(
        self, firstProfileMetrics: list[Metric], secondProfileMetrics: list[Metric]
    ) -> int:
        matchedMetrics = 0
        for i in range(len(firstProfileMetrics)):
            if self.compare_metrics(firstProfileMetrics[i], secondProfileMetrics[i]):
                matchedMetrics += 1
        return matchedMetrics

    async def get(self, profile_id):
        async with self._create_session() as session:
            # get profile metrics
            query = select(Metric).where(Metric.profile_id == profile_id)
            profileMetrics = (await session.execute(query)).scalars()
            if not profileMetrics:
                raise EntityNotFoundException("Profile not found")

            # get all metrics
            allMetrics = {}
            query = select(Metric)
            metrics = (await session.execute(query)).scalars()
            for metric in metrics:
                if (
                    metric.profile_id not in allMetrics
                    and metric.profile_id != profile_id
                ):
                    allMetrics[metric.profile_id] = []
                allMetrics[metric.profile_id].append(metric)

            result = []
            for profileId, metrics in allMetrics.items():
                # matchedMetrics is amount of metrics which are similar to profileMetrics
                # they are used for sorting
                matchedMetrics = self.compare(profileMetrics, metrics)
                if matchedMetrics > MINIMUM_MATCHED_METRICS:
                    result.append((profileId, matchedMetrics))

            # sorting by matchedMetrics so that most similar profiles will be at the beginning of array
            result.sort(key=lambda x: x[1], reverse=True)

        return result


matching_repository = SqlMatchingRepository()
