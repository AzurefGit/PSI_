"""Module containing rating service implementation."""

from typing import Iterable

from culinaryblogapi.core.domain.rating import Rating, RatingBroker
from culinaryblogapi.core.repositories.irating import IRatingRepository
from culinaryblogapi.infrastructure.services.irating import IRatingService


class RatingService(IRatingService):
    """A class implementing the rating service."""

    _repository: IRatingRepository

    def __init__(self, repository: IRatingRepository) -> None:
        """The initializer of the `rating service`.

        Args:
            repository (IRatingRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_rating_by_id(self, rating_id: int) -> Rating | None:
        """The method getting rating by given id.

        Args:
            rating_id (int): The id of the rating.

        Returns:
            Rating | None: The rating details.
        """

        return await self._repository.get_rating_by_id(rating_id)

    async def get_ratings_for_post(self, post_id: int) -> Iterable[Rating]:
        """The method getting all ratings for a specific post.

        Args:
            post_id (int): The id of the post.

        Returns:
            Iterable[Rating]: The collection of ratings for the post.
        """

        return await self._repository.get_ratings_for_post(post_id)

    async def add_rating(self, data: RatingBroker) -> Rating | None:
        """The method adding new rating to the data storage.

        Args:
            data (RatingBroker): The details of the rating.

        Returns:
            Rating | None: The newly created or updated rating.
        """

        return await self._repository.add_rating(data)

    async def calculate_avg_rating(self, post_id: int) -> float:
        """The method for calculating average rating for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            float: The average rating.
        """

        return await self._repository.calculate_avg_rating(post_id)

    async def get_ratings_count(self, post_id: int) -> int:
        """The method for counting ratings for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            int: The number of ratings for the post.
        """
        
        return await self._repository.get_ratings_count(post_id)
