__all__ = ["SqlMatchingRepository", "matching_repository"]


from sqlalchemy import select
from src.repositories.baserepo import SqlBaseRepository

from src.exceptions import EntityNotFoundException, NoMetricException, NotImplementedException
from src.storage.sql.models import Metric


MINIMUM_MATCHED_METRICS = 3
COMPARE_METRICS_VALUE = 0.3


class SqlMatchingRepository(SqlBaseRepository):

    def compare_metrics(self, firstMetric: Metric, secondMetric: Metric) -> bool:
        if abs(firstMetric.value - secondMetric.value) > COMPARE_METRICS_VALUE:
            return False
        return True


    def compare(self, firstProfileMetrics: list[Metric], secondProfileMetrics: list[Metric]) -> int:
        matchedMetrics = 0
        for i in range(len(firstProfileMetrics)):
            if self.compare_metrics(firstProfileMetrics[i],  secondProfileMetrics[i]):
                matchedMetrics += 1
        return matchedMetrics

    async def get(self, profile_id):
        async with self._create_session() as session:
            # get profile metrics
            profileMetrics = await session.execute(select(Metric).filter(Metric.profile_id == profile_id))
            if not profileMetrics:
                raise EntityNotFoundException("Profile not found")


            # get all metrics
            allMetrics = {}
            metrics = await session.execute(select(Metric).all())
            for metric in metrics:
                if metric.profile_id not in allMetrics and metric.profile_id != profile_id:
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