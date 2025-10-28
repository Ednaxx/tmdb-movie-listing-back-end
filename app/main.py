from functools import lru_cache
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import Settings
from .db import create_db_and_tables
from .tmdb.tmdb_router import router as tmdb_router
from .user.router import router as user_router
from .favorites.router import router as favorites_router


@lru_cache
def get_settings():
    return Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tmdb_router, prefix="/tmdb", tags=["tmdb"])
app.include_router(user_router)
app.include_router(favorites_router)


@app.get("/health")
def read_health():
    return {"status": "healthy"}
