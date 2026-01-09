"""Module containing bookmark repository abstraction."""

from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.bookmark import Bookmark, BookmarkIn
from culinaryblogapi.core.domain.post import Post


class IBookmarkRepository(ABC):
    """A class representing bookmark repository."""

    @abstractmethod
    async def add_bookmark(self, data: BookmarkIn) -> Bookmark | None:
        """The method adding new bookmark to the data storage.

        Args:
            data (BookmarkIn): The details of the new bookmark.

        Returns:
            Bookmark | None: Full details of the new added bookmark.
        """

    @abstractmethod
    async def remove_bookmark(self, user_id: str, post_id: int) -> bool:
        """The method removing bookmark from the data storage.

        Args:
            user_id (str): The id of the user.
            post_id (int): The id of the post.

        Returns:
            bool: Result of the operation.
        """

    @abstractmethod
    async def get_user_bookmarks(self, user_id: str) -> Iterable[Post]:
        """The method getting all bookmarked posts for a user.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Post]: The list of bookmarked posts.
        """
