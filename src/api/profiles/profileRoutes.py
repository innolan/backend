from fastapi import APIRouter

from src.schemas.profile import UserProfile
from src.repositories.profiles.profileRepository import profile_repository

profileRouter = APIRouter(prefix="/profiles")

@profileRouter.post("/create")
async def createProfile(profile: UserProfile):
    await profile_repository.create(profile)

@profileRouter.get("/get/{id}")
async def getProfile(id: int):
    return await profile_repository.get(id)

@profileRouter.put("/update/{id}")
async def updateProfile(id: int, profile: UserProfile):
    await profile_repository.update(id, profile)

@profileRouter.delete("/delete/{id}")
async def deleteProfile(id: int):
    await profile_repository.delete(id)

