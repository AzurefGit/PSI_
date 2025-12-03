"""Module containing post repository implementation."""

from typing import Any, Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.post import Post, PostIn
from culinaryblogapi.core.repositories.ipost import IPostRepository
from culinaryblogapi.core.domain.comment import Comment, CommentIn
from culinaryblogapi.db import (
    posts_table,
    comments_table,
    database
)


class PostRepository(IPostRepository):
    """A class representing post DB repository."""

    async def get_post_by_id(self, post_id: int) -> Any | None:
        """The method getting post from the data storage by ID.

        Returns:
            Any: Post in the data storage.
        """

        post = await self._get_by_id(post_id)
        return Post(**dict(post)) if post else None

    async def get_all_posts(self) -> Iterable[Post]:
        """The method getting posts from the data storage.

        Returns:
            Iterable[Post]: Posts in the data storage.
        """

        query = posts_table.select().order_by(posts_table.c.name.asc())
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]

    async def add_comment(self, data: PostIn) -> Any | None:
        """The abstract adding new post to the data storage.

        Args:
            data (PostIn): The attributes of the post.

        Returns:
            Any | None: The newly created post.
        """

        query = posts_table.insert().values(**data.model_dump())
        new_post_id = await database.execute(query)
        new_post = await self._get_by_id(new_post_id)

        return Post(**dict(new_post)) if new_post else None

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
            .order_by(comments_table.c.name.asc())
        )

        return await database.fetch_one(query)
