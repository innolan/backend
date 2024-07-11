__all__ = ["router"]

from fastapi import APIRouter, Depends

from src.middleware.auth_guard import get_id
from src import repositories as reps
from src import schemas

router = APIRouter(prefix="/metric", tags=["Metrics"])
@router.post("/", description="Add new metric to a profile")
async def addMetric(metric: schemas.MetricDTO, id: str = Depends(get_id)):
    return await reps.metric_repository.create(id, metric)

@router.put("/", description="Update existing metric in a profile")
async def updateMetric(metric: schemas.MetricDTOUpd, id: str = Depends(get_id)):
    return await reps.metric_repository.update(id, metric)