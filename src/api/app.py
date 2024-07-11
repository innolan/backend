from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse

from src.api.routers import routers
from src.api.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse
)

for _router in routers:
    app.include_router(_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
