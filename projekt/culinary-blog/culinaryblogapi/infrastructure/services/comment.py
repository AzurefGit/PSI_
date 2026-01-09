"""Module containing comment implementation."""

from typing import Iterable

from culinaryblogapi.core.domain.comment import Comment, CommentIn
from culinaryblogapi.core.repositories.icomment import ICommentRepository
from culinaryblogapi.infrastructure.dto.commentdto import CommentDTO
from culinaryblogapi.infrastructure.services.icomment import ICommentService


class CommentService(ICommentService):
    """A class implementing the comment service."""

    _repository: ICommentRepository

    def __init__(self, repository: ICommentRepository) -> None:
        """The initializer of the `comment service`.

        Args:
            repository (ICommentRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_comments(self) -> Iterable[Comment]:
        """The method getting all comments from the repository.

        Returns:
            Iterable[CommentDTO]: All comments.
        """

        return await self._repository.get_all_comments()

    async def get_by_id(self, comment_id: int) -> CommentDTO | None:
        """The method getting comment by provided id.

        Args:
            comment_id (int): The id of the comment.

        Returns:
            CommentDTO | None: The comment details.
        """

        return await self._repository.get_comment_by_id(comment_id)

    async def get_by_user(self, user_id: str) -> Iterable[Comment]:
        """The method getting comments by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Comment]: The comment collection.
        """

        return await self._repository.get_by_user(user_id)

    async def add_comment(self, data: CommentIn) -> Comment | None:
        """The method adding new comment to the repository.

        Args:
            data (CommentIn): The attributes of the comment.

        Returns:
            Comment | None: The newly created comment.
        """

        return await self._repository.add_comment(data)

    async def update_comment(self, comment_id: int, data: CommentIn) -> Comment | None:
        """The method updating comment data in the repository.

        Args:
            comment_id (int): The comment id.
            data (CommentIn): The attributes of the comment.

        Returns:
            Comment | None: The updated comment.
        """

        return await self._repository.update_comment(comment_id=comment_id, data=data)

    async def delete_comment(self, comment_id: int) -> bool:
        """The method removing comment from the repository.

        Args:
            comment_id (int): The comment id.

        Returns:
            bool: Result of the operation.
        """

        return await self._repository.delete_comment(comment_id)

    async def add_like(self, comment_id: int, user_id: str) -> bool:
        """The method for adding a like to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.add_like(comment_id, user_id)

    async def add_dislike(self, comment_id: int, user_id: str) -> bool:
        """The method for adding a dislike to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.add_dislike(comment_id, user_id)
