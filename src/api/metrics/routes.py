__all__ = ["router"]

from fastapi import APIRouter, Depends

from src import schemas
from src.utils import messages
from src import repositories as reps
from src.middleware.auth_guard import get_id

router = APIRouter(
    tags=["Metrics"],
)


@router.post(
    "/metric",
    description="Add new metric to a profile",
    responses={
        201: {"model": schemas.MetricDTO},
        401: {"model": messages.Unauthorized},
        404: {"model": messages.NotFound},
    },
    status_code=201,
)
async def addMetric(metric: schemas.MetricDTOAdd, id: str = Depends(get_id)):
    return await reps.metric_repository.create(id, metric)


@router.put(
    "/metric",
    description="Update existing metric in a profile",
    responses={
        200: {"model": schemas.MetricDTO},
        401: {"model": messages.Unauthorized},
        404: {"model": messages.NotFound},
    },
)
async def updateMetric(metric: schemas.MetricDTO, id: str = Depends(get_id)):
    return await reps.metric_repository.update(id, metric)
