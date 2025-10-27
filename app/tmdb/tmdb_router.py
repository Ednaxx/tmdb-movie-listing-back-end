from fastapi import APIRouter, Query, Path

from .tmdb_client import search_movies, get_movie

router = APIRouter()


@router.get("/search")
def movie_search(query: str = Query(..., min_length=1), page: int = Query(1, ge=1)):
    """Search movies by query string.

    Query parameters:
    - query: the search text
    - page: optional page number (default 1)
    """
    return search_movies(query=query, page=page)


@router.get("/movie/{movie_id}")
def movie_detail(movie_id: int = Path(..., ge=0)):
    """Get movie details by TMDB movie ID."""
    return get_movie(movie_id)
