from typing import Annotated

from fastapi import APIRouter, Query, Path, Depends

from .tmdb_client import (
    search_movies,
    get_movie,
    get_movie_credits,
    get_movie_videos,
    get_movie_images,
    get_movie_recommendations,
    get_movie_similar,
    get_movie_reviews,
)
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
    append_to_response: str = Query(
        None,
        description="Comma-separated list: credits,videos,images,recommendations,similar,reviews",
    ),
):
    """Get detailed movie information by TMDB movie ID. Requires authentication.

    Optional append_to_response parameter allows fetching multiple resources in one request.
    Example: ?append_to_response=credits,videos,images
    """
    return get_movie(movie_id, append_to_response=append_to_response)


@router.get("/movie/{movie_id}/credits")
def movie_credits(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
):
    """Get the cast and crew for a movie. Requires authentication."""
    return get_movie_credits(movie_id)


@router.get("/movie/{movie_id}/videos")
def movie_videos(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
):
    """Get videos (trailers, teasers, clips) for a movie. Requires authentication."""
    return get_movie_videos(movie_id)


@router.get("/movie/{movie_id}/images")
def movie_images(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
):
    """Get images (posters and backdrops) for a movie. Requires authentication."""
    return get_movie_images(movie_id)


@router.get("/movie/{movie_id}/recommendations")
def movie_recommendations(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
    page: int = Query(1, ge=1),
):
    """Get recommended movies based on a movie. Requires authentication."""
    return get_movie_recommendations(movie_id, page=page)


@router.get("/movie/{movie_id}/similar")
def movie_similar(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
    page: int = Query(1, ge=1),
):
    """Get similar movies. Requires authentication."""
    return get_movie_similar(movie_id, page=page)


@router.get("/movie/{movie_id}/reviews")
def movie_reviews(
    _current_user: Annotated[User, Depends(get_current_active_user)],
    movie_id: int = Path(..., ge=0),
    page: int = Query(1, ge=1),
):
    """Get user reviews for a movie. Requires authentication."""
    return get_movie_reviews(movie_id, page=page)
