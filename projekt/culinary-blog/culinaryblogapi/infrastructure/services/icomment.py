"""Module containing comment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.comment import Comment, CommentBroker
from culinaryblogapi.infrastructure.dto.commentdto import CommentDTO


class ICommentService(ABC):
    """A class representing comment repository."""

    @abstractmethod
    async def get_all_comments(self) -> Iterable[CommentDTO]:
        """The method getting all comments from the repository.

        Returns:
            Iterable[CommentDTO]: All comments.
        """

    @abstractmethod
    async def get_by_id(self, comment_id: int) -> CommentDTO | None:
        """The method getting comment by given id.

        Args:
            comment_id (int): The id of the comment.

        Returns:
            CommentDTO | None: The comment details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[Comment]:
        """The method getting comments by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Comment]: The comment collection.
        """

    @abstractmethod
    async def add_comment(self, data: CommentBroker) -> Comment:
        """The method adding new comment to the data storage.

        Args:
            data (Comment): The details of the new comment.

        Returns:
            Comment | None: Full details of the new added comment.
        """

    @abstractmethod
    async def update_comment(self, comment_id: int, data: CommentBroker) -> Comment | None:
        """The method updating comment data in the data storage.

        Args:
            comment_id (int): The id of the comment.
            data (CommentBroker): The details of the updated comment.

        Returns:
            Comment | None: The updated comment details.
        """

    @abstractmethod
    async def delete_comment(self, comment_id: int) -> bool:
        """The method removing comment from the data storage.

        Args:
            comment_id (int): The id of the comment.

        Returns:
              bool: Result of the operation.
        """

    @abstractmethod
    async def add_like(self, comment_id: int, user_id: str) -> bool:
        """The method for adding a like to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def add_dislike(self, comment_id: int, user_id: str) -> bool:
        """The method for adding a dislike to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """