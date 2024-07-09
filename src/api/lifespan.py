__all__ = ["lifespan"]

from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.config import dburl
from src.storage.sql.storage import SQLAlchemyStorage


async def setup_repositories() -> SQLAlchemyStorage:
    from src.repositories import (
        user_repository,
        userinfo_repository,
        auth_repository,
        profile_repository,
        metric_repository,
    )

    storage = SQLAlchemyStorage.from_url(dburl)
    auth_repository.update_storage(storage)
    user_repository.update_storage(storage)
    userinfo_repository.update_storage(storage)
    profile_repository.update_storage(storage)
    metric_repository.update_storage(storage)

    return storage


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Application startup
    storage = await setup_repositories()
    yield
    # Application shutdown
    await storage.close_connection()
