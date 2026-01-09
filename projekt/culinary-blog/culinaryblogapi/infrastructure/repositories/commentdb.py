"""Module containing comment repository implementation."""

from typing import Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.comment import Comment, CommentBroker
from culinaryblogapi.core.repositories.icomment import ICommentRepository
from culinaryblogapi.db import (
    comments_table,
    database
)


class CommentRepository(ICommentRepository):
    """A class representing comment DB repository."""

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        """The method getting comment from the data storage by ID.

        Returns:
            Comment | None: Comment in the data storage.
        """

        comment = await self._get_by_id(comment_id)

        return Comment(**dict(comment)) if comment else None

    async def get_all_comments(self) -> Iterable[Comment]:
        """The method getting comments from the data storage.

        Returns:
            Iterable[Comment]: Comments in the data storage.
        """

        query = comments_table.select().order_by(comments_table.c.likes.desc())
        comments = await database.fetch_all(query)

        return [Comment(**dict(comment)) for comment in comments]

    async def get_by_user(self, user_id: str) -> Iterable[Comment]:
        """The abstract getting comments by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[comment]: The comment collection.
        """

        query = (
            comments_table.select()
            .where(comments_table.c.user_id == user_id)
            .order_by(comments_table.c.likes.desc())
        )
        comments = await database.fetch_all(query)

        return [Comment(**dict(comment)) for comment in comments]

    async def add_comment(self, data: CommentBroker) -> Comment | None:
        """The abstract adding new comment to the data storage.

        Args:
            data (CommentBroker): The attributes of the comment.

        Returns:
            Comment | None: The newly created comment.
        """

        values = data.model_dump()
        values["likes"] = 0
        values["dislikes"] = 0

        query = comments_table.insert().values(**values)
        new_comment_id = await database.execute(query)
        new_comment = await self._get_by_id(new_comment_id)

        return Comment(**dict(new_comment)) if new_comment else None

    async def update_comment(self, comment_id: int, data: CommentBroker) -> Comment | None:
        """The abstract updating comment data in the data storage.

        Args:
            comment_id (int): The comment id.
            data (CommentBroker): The attributes of the comment.

        Returns:
            Comment | None: The updated comment.
        """

        if await self._get_by_id(comment_id):
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

        if await self._get_by_id(comment_id):
            query = comments_table \
                .delete() \
                .where(comments_table.c.id == comment_id)
            await database.execute(query)

            return True

        return False

    async def add_like(self, comment_id: int, user_id: str) -> bool:
        """The abstract method for adding a like to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """

        if await self._get_by_id(comment_id):
            query = (
                comments_table.update()
                .where(comments_table.c.id == comment_id)
                .values(likes=comments_table.c.likes + 1)
            )
            await database.execute(query)
            return True
        return False

    async def add_dislike(self, comment_id: int, user_id: str) -> bool:
        """The abstract method for adding a dislike to a comment.

        Args:
            comment_id (int): The id of the comment.
            user_id (str): The id of the user.

        Returns:
            bool: Success of the operation.
        """
        if await self._get_by_id(comment_id):
            query = (
                comments_table.update()
                .where(comments_table.c.id == comment_id)
                .values(dislikes=comments_table.c.dislikes + 1)
            )
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, comment_id: int) -> Record | None:
        """A private method getting comment from the DB based on its ID.

        Args:
            comment_id (int): The ID of the comment.

        Returns:
            Record | None: Comment record if exists.
        """

        query = (
            comments_table.select()
            .where(comments_table.c.id == comment_id)
        )

        return await database.fetch_one(query)
