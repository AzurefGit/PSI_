"""Module containing comment repository implementation."""

from typing import Any, Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.comment import Comment, CommentIn
from culinaryblogapi.core.repositories.icomment import ICommentRepository
from culinaryblogapi.db import (
    comments_table,
    database
)


class CommentRepository(ICommentRepository):
    """A class representing comment DB repository."""

    async def get_comment_by_id(self, comment_id: int) -> Any | None:
        """The method getting comment from the data storage by ID.

        Returns:
            Any: Comment in the data storage.
        """

        comment = await self._get_by_id(comment_id)
        return Comment(**dict(comment)) if comment else None

    async def get_all_comments(self) -> Iterable[Comment]:
        """The method getting comments from the data storage.

        Returns:
            Iterable[Comment]: Comments in the data storage.
        """

        query = comments_table.select().order_by(comments_table.c.rating.asc())
        comments = await database.fetch_all(query)

        return [Comment(**dict(comment)) for comment in comments]

    async def get_by_user(self, user_id: int) -> Iterable[Comment]:
        """The abstract getting comments by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[comment]: The comment collection.
        """

        query = (
            comments_table.select()
            .where(comments_table.c.user_id == user_id)
            .order_by(comments_table.c.rating.asc())
        )
        comments = await database.fetch_all(query)

        return [Comment(**dict(comment)) for comment in comments]

    async def add_comment(self, data: CommentIn) -> Any | None:
        """The abstract adding new comment to the data storage.

        Args:
            data (CommentIn): The attributes of the comment.

        Returns:
            Any | None: The newly created comment.
        """

        query = comments_table.insert().values(**data.model_dump())
        new_comment_id = await database.execute(query)
        new_comment = await self._get_by_id(new_comment_id)

        return Comment(**dict(new_comment)) if new_comment else None

    async def update_comment(self, comment_id: int, data: CommentIn) -> Any | None:
        """The abstract updating comment data in the data storage.

        Args:
            comment_id (int): The comment id.
            data (CommentIn): The attributes of the comment.

        Returns:
            Any | None: The updated comment.
        """
        if self._get_by_id(comment_id):
            query = (
                comments_table.update()
                .where(comments_table.c.id == comment_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            comment = await self._get_by_id(comment_id)

            return Comment(**dict(comment)) if comment else None

        return None

    async def delete_comment(self, comment_id: int) -> bool:
        """The abstract removing comment from the data storage.

        Args:
            comment_id (int): The comment id.
        """

        if self._get_by_id(comment_id):
            query = comments_table \
                .delete() \
                .where(comments_table.c.id == comment_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, comment_id: int) -> Record | None:
        """A private method getting comment from the DB based on its ID.

        Args:
            comment_id (int): The ID of the comment.

        Returns:
            Any | None: Comment record if exists.
        """

        query = (
            comments_table.select()
            .where(comments_table.c.id == comment_id)
            .order_by(comments_table.c.rating.asc())
        )

        return await database.fetch_one(query)
