from datetime import timedelta
from typing import Annotated
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from ..db import SessionDep
from .models import User, UserCreate, UserPublic, Token, ShareToken
from .auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_settings,
    get_current_active_user,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register_user(user_create: UserCreate, session: SessionDep):
    """Register a new user."""
    statement = select(User).where(User.username == user_create.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    statement = select(User).where(User.email == user_create.email)
    existing_email = session.exec(statement).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(user_create.password)
    user = User.model_validate(user_create, update={"hashed_password": hashed_password})

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    """Login and get access token (OAuth2 compatible)."""
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/share-token", response_model=ShareToken)
def generate_share_token(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    """Generate or retrieve the share token for the current user's favorites list."""
    if not current_user.share_token:
        # Generate a new unique token
        while True:
            token = secrets.token_urlsafe(24)
            existing = session.exec(
                select(User).where(User.share_token == token)
            ).first()
            if not existing:
                current_user.share_token = token
                break

        session.add(current_user)
        session.commit()
        session.refresh(current_user)

    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/favorites/shared/{current_user.share_token}"

    return ShareToken(share_token=current_user.share_token, share_url=share_url)


@router.delete("/share-token", status_code=status.HTTP_204_NO_CONTENT)
def revoke_share_token(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep,
):
    """Revoke the share token, making the favorites list private again."""
    if not current_user.share_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No share token exists",
        )

    current_user.share_token = None
    session.add(current_user)
    session.commit()
    return None
