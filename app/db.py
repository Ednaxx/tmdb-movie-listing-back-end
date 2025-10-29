from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from functools import lru_cache
from sqlalchemy_utils import database_exists, create_database

from .config import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_engine():
    settings = get_settings()
    connect_args = {}

    engine = create_engine(settings.database_url, connect_args=connect_args, echo=True)

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
