__all__ = ["router"]

from fastapi import APIRouter, Depends, HTTPException

from src.middleware.auth_guard import get_id
from src.repositories.user.repository import user_repository
from src.exceptions import Message
from src import repositories as reps
from src import schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserInfoDTO)
async def getUserInfo(id: str = Depends(get_id)):
    return await reps.userinfo_repository.get(id)


@router.put("/me", response_model=schemas.UserInfoDTO)
async def updateUserInfo(userinfo: schemas.UserInfoDTO, id: str = Depends(get_id)):
    return await reps.userinfo_repository.update(id, userinfo)

@router.post("/me/metric", description="Add new metric to a profile")
async def addMetric(metric: schemas.MetricDTO, id: str = Depends(get_id)):
    return await reps.metric_repository.create(id, metric)

@router.put("/me/metric", description="Update existing metric in a profile")
async def updateMetric(metric: schemas.MetricDTO, id: str = Depends(get_id)):
    return await reps.metric_repository.update(id, metric)