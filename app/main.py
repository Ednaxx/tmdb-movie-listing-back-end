from functools import lru_cache
from .config import Settings

from fastapi import FastAPI

from .tmdb.tmdb_router import router as tmdb_router

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


app.include_router(tmdb_router, prefix="/tmdb", tags=["tmdb"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
