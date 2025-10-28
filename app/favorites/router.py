from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..db import SessionDep
from ..user.auth import get_current_active_user
from ..user.models import User
from .models import FavoriteMovie, FavoriteMovieCreate, FavoriteMoviePublic


router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post(
    "/", response_model=FavoriteMoviePublic, status_code=status.HTTP_201_CREATED
)
def add_favorite_movie(
    favorite_create: FavoriteMovieCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    """Add a movie to user's favorites."""
    statement = select(FavoriteMovie).where(
        FavoriteMovie.user_id == current_user.id,
        FavoriteMovie.tmdb_movie_id == favorite_create.tmdb_movie_id,
    )
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Movie already in favorites",
        )

    favorite = FavoriteMovie(
        user_id=current_user.id,
        tmdb_movie_id=favorite_create.tmdb_movie_id,
        movie_title=favorite_create.movie_title,
        movie_poster_path=favorite_create.movie_poster_path,
    )
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite


@router.get("/", response_model=List[FavoriteMoviePublic])
def get_favorite_movies(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    """Get all favorite movies for the current user."""
    statement = select(FavoriteMovie).where(FavoriteMovie.user_id == current_user.id)
    favorites = session.exec(statement).all()
    return favorites


@router.delete("/{tmdb_movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite_movie(
    tmdb_movie_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    """Remove a movie from user's favorites."""
    statement = select(FavoriteMovie).where(
        FavoriteMovie.user_id == current_user.id,
        FavoriteMovie.tmdb_movie_id == tmdb_movie_id,
    )
    favorite = session.exec(statement).first()
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not in favorites",
        )

    session.delete(favorite)
    session.commit()
    return None


@router.get("/shared/{share_token}", response_model=List[FavoriteMoviePublic])
def get_shared_favorites(
    share_token: str,
    session: SessionDep,
):
    """Get favorite movies for a user via their public share token. No authentication required."""
    statement = select(User).where(User.share_token == share_token)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired share link",
        )

    statement = select(FavoriteMovie).where(FavoriteMovie.user_id == user.id)
    favorites = session.exec(statement).all()
    return favorites
