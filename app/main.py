from functools import lru_cache
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tmdb_router)
app.include_router(user_router)
app.include_router(favorites_router)


@app.get("/health")
def read_health():
    return {"status": "healthy"}
