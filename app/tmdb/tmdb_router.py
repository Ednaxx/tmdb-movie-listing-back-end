from typing import Annotated

from fastapi import APIRouter, Query, Path, Depends

from .tmdb_client import search_movies, get_movie
from ..user.auth import get_current_active_user
from ..user.models import User

router = APIRouter(prefix="/tmdb", tags=["tmdb"])


@router.get("/search")
def movie_search(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
):
    """Search movies by query string. Requires authentication.

    Query parameters:
    - query: the search text
    - page: optional page number (default 1)
    """
    return search_movies(query=query, page=page)


@router.get("/movie/{movie_id}")
def movie_detail(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
):
    """Get movie details by TMDB movie ID. Requires authentication."""
    return get_movie(movie_id)
