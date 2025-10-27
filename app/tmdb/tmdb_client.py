import logging
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


def get_movie(movie_id: int) -> Dict[str, Any]:
    _ensure_api_key()
    m = tmdb.Movies(movie_id)
    try:
        info = m.info()
        return info
    except Exception as exc: 
        raise HTTPException(status_code=500, detail=f"TMDB movie fetch failed: {exc}")
