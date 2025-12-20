"""Module containing post repository implementation."""

from typing import Any, Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.post import Post, PostIn
from culinaryblogapi.core.repositories.ipost import IPostRepository
# from culinaryblogapi.core.domain.comment import Comment, CommentIn
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

        query = posts_table.select().order_by(posts_table.c.title.asc())
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]

    async def get_by_user(self, user_id: int) -> Iterable[Post]:
        """The abstract getting comments by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[comment]: The comment collection.
        """

        query = (
            posts_table.select()
            .where(posts_table.c.user_id == user_id)
            .order_by(posts_table.c.title.asc())
        )
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]

    async def add_post(self, data: PostIn) -> Any | None:
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

    async def update_post(self, post_id: int, data: PostIn) -> Any | None:
        """The abstract updating post data in the data storage.

        Args:
            post_id (int): The post id.
            data (PostIn): The attributes of the post.

        Returns:
            Any | None: The updated post.
        """
        if self._get_by_id(post_id):
            query = (
                posts_table.update()
                .where(posts_table.c.id == post_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            post = await self._get_by_id(post_id)

            return Post(**dict(post)) if post else None

        return None

    async def delete_post(self, post_id: int) -> bool:
        """The abstract removing post from the data storage.

        Args:
            post_id (int): The post id.
        """

        if self._get_by_id(post_id):
            query = posts_table \
            .delete() \
            .where(posts_table.c.id == post_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, post_id: int) -> Record | None:
        """A private method getting post from the DB based on its ID.

        Args:
            post_id (int): The ID of the post.

        Returns:
            Any | None: Post record if exists.
        """

        query = (
            posts_table.select()
            .where(posts_table.c.id == post_id)
            .order_by(posts_table.c.title.asc())
        )

        return await database.fetch_one(query)
