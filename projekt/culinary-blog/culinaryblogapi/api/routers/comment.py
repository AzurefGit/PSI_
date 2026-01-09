"""A module containing comment endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from culinaryblogapi.infrastructure.utils import consts
from culinaryblogapi.container import Container
from culinaryblogapi.core.domain.comment import Comment, CommentIn, CommentBroker
from culinaryblogapi.infrastructure.dto.commentdto import CommentDTO
from culinaryblogapi.infrastructure.services.icomment import ICommentService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Comment, status_code=201)
@inject
async def create_comment(
    comment: CommentIn,
    service: ICommentService = Depends(Provide[Container.comment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new comment.

    Args:
        comment (CommentIn): The comment data.
        service (ICommentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new comment attributes.
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

    extended_comment_data = CommentBroker(
        user_id=user_uuid,
        **comment.model_dump(),
    )
    new_comment = await service.add_comment(extended_comment_data)

    return new_comment.model_dump() if new_comment else {}


@router.get("/all", response_model=Iterable[CommentDTO], status_code=200)
@inject
async def get_all_comments(
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> Iterable:
    """An endpoint for getting all comments.

    Args:
        service (ICommentService, optional): The injected service dependency.

    Returns:
        Iterable: The comments attributes collection.
    """

    comments = await service.get_all_comments()

    return comments


@router.get(
        "/{comment_id}",
        response_model=CommentDTO,
        status_code=200,
)
@inject
async def get_comment_by_id(
    comment_id: int,
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> dict | None:
    """An endpoint for getting comment by id.

    Args:
        comment_id (int): The id of the comment.
        service (ICommentService, optional): The injected service dependency.

    Returns:
        dict | None: The comment details.
    """

    if comment := await service.get_by_id(comment_id):
        return comment.model_dump()

    raise HTTPException(status_code=404, detail="Comment not found")


@router.get(
        "/user/{comment_id}",
        response_model=Iterable[Comment],
        status_code=200,
)
@inject
async def get_comment_by_user(
    user_id: str,
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> Iterable:
    """An endpoint for getting comments by user who added them.

    Args:
        user_id (str): The id of the user.
        service (ICommentService, optional): The injected service dependency.

    Returns:
        Iterable: The comment details collection.
    """

    comments = await service.get_by_user(user_id)

    return comments


@router.put("/{comment_id}", response_model=Comment, status_code=201)
@inject
async def update_comment(
    comment_id: int,
    updated_comment: CommentIn,
    service: ICommentService = Depends(Provide[Container.comment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating comment data.

    Args:
        comment_id (int): The id of the comment.
        updated_comment (CommentIn): The updated comment details.
        service (ICommentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if comment does not exist.

    Returns:
        dict: The updated comment details.
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

    if comment_data := await service.get_by_id(comment_id=comment_id):
        if str(comment_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_comment = CommentBroker(
            user_id=user_uuid,
            **updated_comment.model_dump(),
        )
        updated_comment_data = await service.update_comment(
            comment_id=comment_id,
            data=extended_updated_comment,
        )
        return updated_comment_data.model_dump() if updated_comment_data \
            else {}

    raise HTTPException(status_code=404, detail="Comment not found")


@router.delete("/{comment_id}", status_code=204)
@inject
async def delete_comment(
    comment_id: int,
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> None:
    """An endpoint for deleting comments.

    Args:
        comment_id (int): The id of the comment.
        service (ICommentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if comment does not exist.
    """

    if await service.get_by_id(comment_id=comment_id):
        await service.delete_comment(comment_id)

        return

    raise HTTPException(status_code=404, detail="Comment not found")


@router.post("/{comment_id}/like", status_code=200)
@inject
async def add_like(
    comment_id: int,
    service: ICommentService = Depends(Provide[Container.comment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding a like to a comment.

    Args:
        comment_id (int): The id of the comment.
        service (ICommentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: Success message.
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

    if await service.add_like(comment_id, user_uuid):
        return {"message": "Like added"}
    
    raise HTTPException(status_code=404, detail="Comment not found")


@router.post("/{comment_id}/dislike", status_code=200)
@inject
async def add_dislike(
    comment_id: int,
    service: ICommentService = Depends(Provide[Container.comment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding a dislike to a comment.

    Args:
        comment_id (int): The id of the comment.
        service (ICommentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: Success message.
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

    if await service.add_dislike(comment_id, user_uuid):
        return {"message": "Dislike added"}
    
    raise HTTPException(status_code=404, detail="Comment not found")