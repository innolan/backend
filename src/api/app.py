from fastapi import FastAPI, APIRouter

from src.api.routers import routers
from src.api.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
)

apiRouter = APIRouter(prefix="/api")
for _router in routers:
    apiRouter.include_router(_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(apiRouter)
