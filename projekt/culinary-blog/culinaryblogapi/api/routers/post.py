"""A module containing post endpoints."""

from typing import Iterable

from dependency_injector import containers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from culinaryblogapi.infrastructure.utils import consts
from culinaryblogapi.container import Container
from culinaryblogapi.core.domain.post import Post, PostIn, PostBroker
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


