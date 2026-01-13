"""A module containing bookmark endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from culinaryblogapi.container import Container
from culinaryblogapi.core.domain.bookmark import BookmarkIn
from culinaryblogapi.core.domain.post import Post
from culinaryblogapi.infrastructure.services.ibookmark import IBookmarkService
from culinaryblogapi.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/{post_id}", status_code=201)
@inject
async def add_bookmark(
    post_id: int,
    service: IBookmarkService = Depends(Provide[Container.bookmark_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding a bookmark.

    Args:
        post_id (int): The id of the post to bookmark.
        service (IBookmarkService, optional): The injected service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new bookmark attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    bookmark_data = BookmarkIn(
        user_id=user_uuid,
        post_id=post_id
    )

    new_bookmark = await service.add_bookmark(bookmark_data)

    if new_bookmark:
        return new_bookmark.model_dump()
    
    return {}


@router.delete("/{post_id}", status_code=204)
@inject
async def remove_bookmark(
    post_id: int,
    service: IBookmarkService = Depends(Provide[Container.bookmark_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for removing a bookmark.

    Args:
        post_id (int): The id of the post to remove from bookmarks.
        service (IBookmarkService, optional): The injected service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    await service.remove_bookmark(user_id=user_uuid, post_id=post_id)


@router.get("/all", response_model=Iterable[Post], status_code=200)
@inject
async def get_user_bookmarks(
    service: IBookmarkService = Depends(Provide[Container.bookmark_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Iterable:
    """An endpoint for getting all bookmarks for a user.

    Args:
        service (IBookmarkService, optional): The injected service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: The list of bookmarked posts.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return await service.get_user_bookmarks(user_id=user_uuid)
