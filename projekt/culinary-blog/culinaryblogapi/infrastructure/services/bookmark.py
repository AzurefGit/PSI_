"""Module containing bookmark service implementation."""

from typing import Iterable

from culinaryblogapi.core.domain.bookmark import Bookmark, BookmarkIn
from culinaryblogapi.core.domain.post import Post
from culinaryblogapi.core.repositories.ibookmark import IBookmarkRepository
from culinaryblogapi.infrastructure.services.ibookmark import IBookmarkService


class BookmarkService(IBookmarkService):
    """A class implementing the bookmark service."""

    _repository: IBookmarkRepository

    def __init__(self, repository: IBookmarkRepository) -> None:
        """The initializer of the `bookmark service`.

        Args:
            repository (IBookmarkRepository): The reference to the repository.
        """
        self._repository = repository

    async def add_bookmark(self, data: BookmarkIn) -> Bookmark | None:
        """The method adding new bookmark.

        Args:
            data (BookmarkIn): The details of the new bookmark.

        Returns:
            Bookmark | None: Full details of the new added bookmark.
        """
        return await self._repository.add_bookmark(data)

    async def remove_bookmark(self, user_id: str, post_id: int) -> bool:
        """The method removing bookmark.

        Args:
            user_id (str): The id of the user.
            post_id (int): The id of the post.

        Returns:
            bool: Result of the operation.
        """
        return await self._repository.remove_bookmark(user_id, post_id)

    async def get_user_bookmarks(self, user_id: str) -> Iterable[Post]:
        """The method getting all bookmarked posts for a user.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Post]: The list of bookmarked posts.
        """
        return await self._repository.get_user_bookmarks(user_id)
