"""Module containing bookmark repository implementation."""

from typing import Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.bookmark import Bookmark, BookmarkIn
from culinaryblogapi.core.domain.post import Post
from culinaryblogapi.core.repositories.ibookmark import IBookmarkRepository
from culinaryblogapi.db import (
    bookmarks_table,
    posts_table,
    database
)


class BookmarkRepository(IBookmarkRepository):
    """A class representing bookmark DB repository."""

    async def add_bookmark(self, data: BookmarkIn) -> Bookmark | None:
        """The method adding new bookmark to the data storage.

        Args:
            data (BookmarkIn): The attributes of the bookmark.

        Returns:
            Bookmark | None: The newly created bookmark.
        """

        query = (
            bookmarks_table.select()
            .where(bookmarks_table.c.user_id == data.user_id)
            .where(bookmarks_table.c.post_id == data.post_id)
        )

        existing = await database.fetch_one(query)

        if existing:
            return Bookmark(**dict(existing))

        query = bookmarks_table.insert().values(**data.model_dump())
        new_id = await database.execute(query)
        
        new_bookmark = await self._get_by_id(new_id)

        return Bookmark(**dict(new_bookmark)) if new_bookmark else None

    async def remove_bookmark(self, user_id: str, post_id: int) -> bool:
        """The method removing bookmark from the data storage.

        Args:
            user_id (str): The id of the user.
            post_id (int): The id of the post.

        Returns:
            bool: Result of the operation.
        """

        query = bookmarks_table.delete().where(
            (bookmarks_table.c.user_id == user_id) &
            (bookmarks_table.c.post_id == post_id)
        )
        await database.execute(query)

        return True

    async def get_user_bookmarks(self, user_id: str) -> Iterable[Post]:
        """The method getting all bookmarked posts for a user.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Post]: The list of bookmarked posts.
        """

        query = (
            posts_table.join(bookmarks_table, posts_table.c.id == bookmarks_table.c.post_id)
            .select()
            .where(bookmarks_table.c.user_id == user_id)
        )
    
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]

    async def _get_by_id(self, bookmark_id: int) -> Record | None:
        """A private method getting bookmark from the data storage by ID.

        Args:
            bookmark_id (int): The id of the bookmark.

        Returns:
            Record | None: Bookmark record if exists.
        """

        query = (bookmarks_table.select()
        .where(bookmarks_table.c.id == bookmark_id)
        )

        return await database.fetch_one(query)
