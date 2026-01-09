"""Module containing rating service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.rating import Rating, RatingBroker


class IRatingService(ABC):
    """A class representing rating service."""

    @abstractmethod
    async def get_rating_by_id(self, rating_id: int) -> Rating | None:
        """The method getting rating by given id.

        Args:
            rating_id (int): The id of the rating.

        Returns:
            Rating | None: The rating details.
        """

    @abstractmethod
    async def get_ratings_for_post(self, post_id: int) -> Iterable[Rating]:
        """The method getting all ratings for a specific post.

        Args:
            post_id (int): The id of the post.

        Returns:
            Iterable[Rating]: The collection of ratings for the post.
        """

    @abstractmethod
    async def add_rating(self, data: RatingBroker) -> Rating | None:
        """The method adding new rating to the data storage.

        Args:
            data (RatingBroker): The details of the rating.

        Returns:
            Rating | None: The newly created or updated rating.
        """

    @abstractmethod
    async def calculate_avg_rating(self, post_id: int) -> float:
        """The method for calculating average rating for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            float: The average rating.
        """

    @abstractmethod
    async def get_ratings_count(self, post_id: int) -> int:
        """The method for counting ratings for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            int: The number of ratings for the post.
        """
