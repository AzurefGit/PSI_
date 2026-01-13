"""Module containing rating repository implementation."""

from typing import Iterable
from asyncpg import Record
from sqlalchemy import func, select

from culinaryblogapi.core.domain.rating import Rating, RatingBroker
from culinaryblogapi.core.repositories.irating import IRatingRepository
from culinaryblogapi.db import (
    ratings_table,
    database
)


class RatingRepository(IRatingRepository):
    """A class representing rating DB repository."""

    async def get_rating_by_id(self, rating_id: int) -> Rating | None:
        """The abstract method for getting a rating from the data storage by ID.

        Args:
            rating_id (int): The id of the rating.

        Returns:
            Rating | None: The rating data if exists.
        """

        rating = await self._get_by_id(rating_id)
        return Rating(**dict(rating)) if rating else None

    async def get_ratings_for_post(self, post_id: int) -> Iterable[Rating]:
        """The abstract method for getting all ratings for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            Iterable[Rating]: The collection of ratings for the post.
        """

        query = (
            ratings_table.select()
            .where(ratings_table.c.post_id == post_id)
        )
        ratings = await database.fetch_all(query)

        return [Rating(**dict(rating)) for rating in ratings]

    async def add_rating(self, data: RatingBroker) -> Rating | None:
        """The abstract method for adding new rating to the data storage.

        If user already rated this post, the rating will be updated.

        Args:
            data (RatingBroker): The attributes of the rating.

        Returns:
            Rating | None: The newly created or updated rating.
        """
        
        query = (
            ratings_table.select()
            .where(ratings_table.c.post_id == data.post_id)
            .where(ratings_table.c.user_id == data.user_id)
        )
        existing_rating = await database.fetch_one(query)

        if existing_rating:
            query = (
                ratings_table.update()
                .where(ratings_table.c.id == existing_rating["id"])
                .values(rating=data.rating)
            )

            await database.execute(query)
            rating_id = existing_rating["id"]
        else:
            query = ratings_table.insert().values(**data.model_dump())
            rating_id = await database.execute(query)


        new_rating = await self._get_by_id(rating_id)
        
        return Rating(**dict(new_rating)) if new_rating else None

    async def calculate_avg_rating(self, post_id: int) -> float:
        """The abstract method for calculating average rating for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            float: The average rating (0.0 if no ratings exist).
        """

        query = select(func.avg(ratings_table.c.rating)).where(ratings_table.c.post_id == post_id)
        result = await database.fetch_val(query)

        return float(result) if result is not None else 0.0

    async def get_ratings_count(self, post_id: int) -> int:
        """The abstract method for counting ratings for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            int: The number of ratings for the post.
        """

        query = select(func.count(ratings_table.c.id)).where(ratings_table.c.post_id == post_id)
        result = await database.fetch_val(query)

        return int(result) if result is not None else 0

    async def _get_by_id(self, rating_id: int) -> Record | None:
        """A private method getting rating from the DB based on its ID.

        Args:
            rating_id (int): The ID of the rating.

        Returns:
            Record | None: Rating record if exists.
        """

        query = (
            ratings_table.select()
            .where(ratings_table.c.id == rating_id)
        )

        return await database.fetch_one(query)
