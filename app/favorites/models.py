import uuid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class FavoriteMovie(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    tmdb_movie_id: int = Field(index=True)
    movie_title: str
    movie_poster_path: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)


class FavoriteMovieCreate(BaseModel):
    tmdb_movie_id: int
    movie_title: str
    movie_poster_path: Optional[str] = None


class FavoriteMoviePublic(BaseModel):
    id: uuid.UUID
    tmdb_movie_id: int
    movie_title: str
    movie_poster_path: Optional[str]
    added_at: datetime
