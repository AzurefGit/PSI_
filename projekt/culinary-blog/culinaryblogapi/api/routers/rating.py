"""A module containing rating endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from culinaryblogapi.infrastructure.utils import consts
from culinaryblogapi.container import Container
from culinaryblogapi.core.domain.rating import Rating, RatingIn, RatingBroker
from culinaryblogapi.infrastructure.services.irating import IRatingService
from culinaryblogapi.infrastructure.services.ipost import IPostService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Rating, status_code=201)
@inject
async def add_rating(
    rating: RatingIn,
    rating_service: IRatingService = Depends(Provide[Container.rating_service]),
    post_service: IPostService = Depends(Provide[Container.post_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding/updating a rating.

    Args:
        rating (RatingIn): The rating data.
        rating_service (IRatingService, optional): The injected rating service.
        post_service (IPostService, optional): The injected post service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new rating attributes.
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

    extended_rating_data = RatingBroker(
        user_id=user_uuid,
        **rating.model_dump(),
    )
    
    new_rating = await rating_service.add_rating(extended_rating_data)
    
    if new_rating:
        avg_rating = await rating_service.calculate_avg_rating(rating.post_id)
        ratings_count = await rating_service.get_ratings_count(rating.post_id)
        
        await post_service.update_post_rating(
            post_id=rating.post_id,
            avg_rating=avg_rating,
            ratings_count=ratings_count
        )

        return new_rating.model_dump()
    
    return {}


@router.get("/post/{post_id}", response_model=Iterable[Rating], status_code=200)
@inject
async def get_ratings_for_post(
    post_id: int,
    service: IRatingService = Depends(Provide[Container.rating_service]),
) -> Iterable:
    """An endpoint for getting all ratings for a post.

    Args:
        post_id (int): The id of the post.
        service (IRatingService, optional): The injected service dependency.

    Returns:
        Iterable: The ratings collection.
    """

    return await service.get_ratings_for_post(post_id)
