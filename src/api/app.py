from fastapi import FastAPI, APIRouter

from src.api.routers import routers
from src.api.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
)

for _router in routers:
    app.include_router(_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
