from fastapi import FastAPI, APIRouter

from src.api.lifespan import lifespan
from src.api.auth.routes import router
from src.api.profiles.profileRoutes import profileRouter

app = FastAPI(
    lifespan=lifespan,
)

apiRouter = APIRouter(prefix="/api")
apiRouter.include_router(router)
apiRouter.include_router(profileRouter)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(apiRouter)
