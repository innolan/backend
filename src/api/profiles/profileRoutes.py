from fastapi import APIRouter, Response, status

from src.schemas.signin import CreateProfile
from src.repositories.profiles.profileRepository import profile_repository

profileRouter = APIRouter(prefix="/profile")

# Disallowed temporarily, since the profile is created on sign in anyway

# @profileRouter.post("/create")
# async def createProfile(profile: CreateProfile, status_code=201):
#     await profile_repository.create(profile)


@profileRouter.get("/get/{id}")
async def getProfile(id: int, response: Response):
    result = await profile_repository.get(id)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if result else {}


@profileRouter.put("/update/{id")
async def updateProfile(id: int, profile: CreateProfile, response: Response):
    result = await profile_repository.update(id, profile)
    if not result:
        response.status_code = status.HTTP_404_NOT_FOUND
    return result if result else {}


@profileRouter.delete("/delete/{id}")
async def deleteProfile(id: int):
    await profile_repository.delete(id)
    return {}
