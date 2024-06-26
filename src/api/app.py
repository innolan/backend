from fastapi import FastAPI

from src.api.lifespan import lifespan
from src.api.auth.routes import router
from src.api.profiles.profileRoutes import profileRouter

app = FastAPI(
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router)
app.include_router(profileRouter)