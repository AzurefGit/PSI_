"""A module containing rating repository abstraction."""

from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.rating import Rating, RatingIn, RatingBroker


class IRatingRepository(ABC):
    """An abstract repository for rating operations."""

    @abstractmethod
    async def get_rating_by_id(self, rating_id: int) -> Rating | None:
        """The abstract method for getting a rating from the data storage by ID.

        Args:
            rating_id (int): The id of the rating.

        Returns:
            Rating | None: The rating data if exists.
        """

    @abstractmethod
    async def get_ratings_for_post(self, post_id: int) -> Iterable[Rating]:
        """The abstract method for getting all ratings for a specific post.

        Args:
            post_id (int): The id of the post.

        Returns:
            Iterable[Rating]: The collection of ratings for the post.
        """

    @abstractmethod
    async def add_rating(self, data: RatingBroker) -> Rating | None:
        """The abstract method for adding new rating to the data storage.

        If user already rated this post, the rating will be updated.

        Args:
            data (RatingBroker): The attributes of the rating.

        Returns:
            Rating | None: The newly created or updated rating.
        """

    @abstractmethod
    async def calculate_avg_rating(self, post_id: int) -> float:
        """The abstract method for calculating average rating for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            float: The average rating (0.0 if no ratings exist).
        """

    @abstractmethod
    async def get_ratings_count(self, post_id: int) -> int:
        """The abstract method for counting ratings for a post.

        Args:
            post_id (int): The id of the post.

        Returns:
            int: The number of ratings for the post.
        """
