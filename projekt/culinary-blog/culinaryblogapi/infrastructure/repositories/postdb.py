"""Module containing post repository implementation."""

from typing import Iterable
from asyncpg import Record

from culinaryblogapi.core.domain.post import Post, PostBroker
from culinaryblogapi.core.repositories.ipost import IPostRepository
from culinaryblogapi.db import (
    posts_table,
    database
)


class PostRepository(IPostRepository):
    """A class representing post DB repository."""

    async def get_post_by_id(self, post_id: int) -> Post | None:
        """The method getting post from the data storage by ID.

        Returns:
            Post | None: Post in the data storage.
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

    async def get_by_title(self, text: str) -> Iterable[Post]:
        """The method getting posts from the data storage by title or by a port of it.
        Args:
            text (str): The title of the posts.

        Returns:
            Iterable[Post]: Posts in the data storage.
        """

        query = (
            posts_table.select()
            .where(posts_table.c.title.ilike(f"%{text}%"))
            .order_by(posts_table.c.title.asc())
        )
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]


    async def get_by_user(self, user_id: str) -> Iterable[Post]:
        """The abstract getting posts by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[post]: The post collection.
        """

        query = (
            posts_table.select()
            .where(posts_table.c.user_id == user_id)
            .order_by(posts_table.c.title.asc())
        )
        posts = await database.fetch_all(query)

        return [Post(**dict(post)) for post in posts]

    async def add_post(self, data: PostBroker) -> Post | None:
        """The abstract adding new post to the data storage.

        Args:
            data (PostBroker): The attributes of the post.

        Returns:
            Post | None: The newly created post.
        """

        values = data.model_dump()
        values["avg_rating"] = 0.0
        values["ratings_count"] = 0

        query = posts_table.insert().values(**values)
        new_post_id = await database.execute(query)
        new_post = await self._get_by_id(new_post_id)

        return Post(**dict(new_post)) if new_post else None

    async def update_post(self, post_id: int, data: PostBroker) -> Post | None:
        """The abstract updating post data in the data storage.

        Args:
            post_id (int): The post id.
            data (PostBroker): The attributes of the post.

        Returns:
            Post | None: The updated post.
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

        post = await self._get_by_id(post_id)
        if post:
            query = posts_table \
            .delete() \
            .where(posts_table.c.id == post_id)
            await database.execute(query)

            return True

        return False

    async def update_post_rating(
        self,
        post_id: int,
        avg_rating: float,
        ratings_count: int
    ) -> bool:
        """The abstract method for updating post's rating statistics.

        Args:
            post_id (int): The id of the post.
            avg_rating (float): The new average rating.
            ratings_count (int): The total number of ratings.

        Returns:
            bool: Success of the operation.
        """

        post = await self._get_by_id(post_id)
        if post:
            query = (
                posts_table.update()
                .where(posts_table.c.id == post_id)
                .values(avg_rating=avg_rating, ratings_count=ratings_count)
            )
            await database.execute(query)
            return True
        return False

    async def _get_by_id(self, post_id: int) -> Record | None:
        """A private method getting post from the DB based on its ID.

        Args:
            post_id (int): The ID of the post.

        Returns:
            Record | None: Post record if exists.
        """

        query = (
            posts_table.select()
            .where(posts_table.c.id == post_id)
            .order_by(posts_table.c.title.asc())
        )

        return await database.fetch_one(query)
