from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.comment import Comment, CommentIn


class ICommentRepository(ABC):
    @abstractmethod
    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        """The abstract getting a comment from the data storage.

        Args:
            comment_id (int): The id of the comment.

        Returns:
            comment | None: The comment data if exists.
        """

    @abstractmethod
    async def get_all_comments(self) -> Iterable[Comment]:
        """The abstract getting all comments from the data storage.

        Returns:
            Iterable[comment]: The collection of the all comments.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[Comment]:
        """The abstract getting comments by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[comment]: The comment collection.
        """

    @abstractmethod
    async def add_comment(self, data: CommentIn) -> None:
        """The abstract adding new comment to the data storage.

        Args:
            data (commentIn): The attributes of the comment.
        """

    @abstractmethod
    async def update_comment(self, comment_id: int, data: CommentIn) -> Comment | None:
        """The abstract updating comment data in the data storage.

        Args:
            comment_id (int): The comment id.
            data (commentIn): The attributes of the comment.

        Returns:
            comment | None: The updated comment.
        """

    @abstractmethod
    async def delete_comment(self, comment_id: int) -> bool:
        """The abstract updating removing comment from the data storage.

        Args:
            comment_id (int): The comment id.

        Returns:
            bool: Success of the operation.
        """
