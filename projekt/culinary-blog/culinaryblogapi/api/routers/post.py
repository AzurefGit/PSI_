"""A module containing post endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from culinaryblogapi.infrastructure.utils import consts
from culinaryblogapi.container import Container
from culinaryblogapi.core.domain.post import Post, PostIn, PostBroker
from culinaryblogapi.infrastructure.dto.postdto import PostDTO
from culinaryblogapi.infrastructure.services.ipost import IPostService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Post, status_code=201)
@inject
async def create_post(
    post: PostIn,
    service: IPostService = Depends(Provide[Container.post_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new post.

    Args:
        post (PostIn): The post data.
        service (IPostService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new post attributes.
    """
    token = credentials.credentials
    print(f"Received token: {token}")  # DEBUG
    print(f"Token length: {len(token)}")  # DEBUG
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_post_data = PostBroker(
        user_id=user_uuid,
        **post.model_dump(),
    )
    new_post = await service.add_post(extended_post_data)

    return new_post.model_dump() if new_post else {}

@router.get("/all", response_model=Iterable[PostDTO], status_code=200)
@inject
async def get_all_posts(
    service: IPostService = Depends(Provide[Container.post_service]),
) -> Iterable:
    """An endpoint for getting all posts.

    Args:
        service (IPostService, optional): The injected service dependency.

    Returns:
        Iterable: The posts attributes collection.
    """

    posts = await service.get_all_posts()

    return posts


@router.get(
        "/{post_id}",
        response_model=PostDTO,
        status_code=200,
)
@inject
async def get_post_by_id(
    post_id: int,
    service: IPostService = Depends(Provide[Container.post_service]),
) -> dict | None:
    """An endpoint for getting post by id.

    Args:
        post_id (int): The id of the post.
        service (IPostService, optional): The injected service dependency.

    Returns:
        dict | None: The post details.
    """

    if post := await service.get_post_by_id(post_id):
        return post.model_dump()

    raise HTTPException(status_code=404, detail="Post not found")


@router.get(
        "/user/{post_id}",
        response_model=Iterable[Post],
        status_code=200,
)
@inject
async def get_posts_by_user(
    user_id: int,
    service: IPostService = Depends(Provide[Container.post_service]),
) -> Iterable:
    """An endpoint for getting posts by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IPostService, optional): The injected service dependency.

    Returns:
        Iterable: The post details collection.
    """

    posts = await service.get_by_user(user_id)

    return posts


@router.put("/{post_id}", response_model=Post, status_code=201)
@inject
async def update_post(
    post_id: int,
    updated_post: PostIn,
    service: IPostService = Depends(Provide[Container.post_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating post data.

    Args:
        post_id (int): The id of the post.
        updated_post (PostIn): The updated post details.
        service (IPostService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if post does not exist.

    Returns:
        dict: The updated post details.
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

    if post_data := await service.get_by_id(post_id=post_id):
        if str(post_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_post = PostBroker(
            user_id=user_uuid,
            **updated_post.model_dump(),
        )
        updated_post_data = await service.update_post(
            post_id=post_id,
            data=extended_updated_post,
        )
        return updated_post_data.model_dump() if updated_post_data \
            else {}

    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/{post_id}", status_code=204)
@inject
async def delete_post(
    post_id: int,
    service: IPostService = Depends(Provide[Container.post_service]),
) -> None:
    """An endpoint for deleting posts.

    Args:
        post_id (int): The id of the post.
        service (IPostService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if post does not exist.
    """

    if await service.get_post_by_id(post_id=post_id):
        await service.delete_post(post_id)

        return

    raise HTTPException(status_code=404, detail="Post not found")
