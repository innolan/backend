from fastapi import FastAPI

from src.api.auth.routes import router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)
