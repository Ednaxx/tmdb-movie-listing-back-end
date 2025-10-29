from typing import Any, Dict

import tmdbsimple as tmdb
from fastapi import HTTPException

from ..config import Settings


def _ensure_api_key() -> None:
    settings = Settings()
    api_key = getattr(settings, "tmdb_api_key", None)
    if not api_key:
        raise HTTPException(status_code=500, detail="TMDB API key not configured")
    tmdb.API_KEY = api_key


def search_movies(query: str, page: int = 1) -> Dict[str, Any]:
    _ensure_api_key()
    s = tmdb.Search()
    try:
        result = s.movie(query=query, page=page)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB search failed: {exc}")


def get_movie(movie_id: int, append_to_response: str = None) -> Dict[str, Any]:
    """Get detailed movie information.

    Args:
        movie_id: The TMDB movie ID
        append_to_response: Optional comma-separated list of additional requests
                          (e.g., "credits,videos,images,recommendations")
    """
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        kwargs = {}
        if append_to_response:
            kwargs["append_to_response"] = append_to_response
        info = m.info(**kwargs)
        return info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB movie fetch failed: {exc}")


def get_movie_credits(movie_id: int) -> Dict[str, Any]:
    """Get the cast and crew for a movie."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        credits = m.credits()
        return credits
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB credits fetch failed: {exc}")


def get_movie_videos(movie_id: int) -> Dict[str, Any]:
    """Get the videos (trailers, teasers, clips, etc.) for a movie."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        videos = m.videos()
        return videos
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB videos fetch failed: {exc}")


def get_movie_images(movie_id: int) -> Dict[str, Any]:
    """Get the images (posters and backdrops) for a movie."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        images = m.images()
        return images
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB images fetch failed: {exc}")


def get_movie_recommendations(movie_id: int, page: int = 1) -> Dict[str, Any]:
    """Get a list of recommended movies for a movie."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        recommendations = m.recommendations(page=page)
        return recommendations
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"TMDB recommendations fetch failed: {exc}"
        )


def get_movie_similar(movie_id: int, page: int = 1) -> Dict[str, Any]:
    """Get a list of similar movies."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        similar = m.similar(page=page)
        return similar
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"TMDB similar movies fetch failed: {exc}"
        )


def get_movie_reviews(movie_id: int, page: int = 1) -> Dict[str, Any]:
    """Get the user reviews for a movie."""
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        reviews = m.reviews(page=page)
        return reviews
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"TMDB reviews fetch failed: {exc}")
