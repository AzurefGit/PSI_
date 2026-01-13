"""Module containing post service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.post import Post, PostBroker
from culinaryblogapi.infrastructure.dto.postdto import PostDTO


class IPostService(ABC):
    """A class representing post repository."""

    @abstractmethod
    async def get_all_posts(self) -> Iterable[Post]:
        """The method getting all posts from the repository.

        Returns:
            Iterable[Post]: All posts.
        """

    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> PostDTO | None:
        """The method getting post by given id.

        Args:
            post_id (int): The id of the post.

        Returns:
            PostDTO | None: The post details.
        """

    @abstractmethod
    async def get_by_title(self, text: str) -> Iterable[Post]:
        """The method getting posts by title or by a part of it.

        Args:
            text (str): The title of the post.

        Returns:
            Iterable[Post]: The post collection.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[Post]:
        """The method getting posts by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Post]: The post collection.
        """

    @abstractmethod
    async def add_post(self, data: PostBroker) -> Post | None:
        """The method adding new post to the data storage.

        Args:
            data (Post): The details of the new post.

        Returns:
            Post | None: Full details of the new added post.
        """

    @abstractmethod
    async def update_post(self, post_id: int, data: PostBroker) -> Post | None:
        """The method updating post data in the data storage.

        Args:
            post_id (int): The id of the post.
            data (PostBroker): The details of the updated post.

        Returns:
            Post | None: The updated post details.
        """

    @abstractmethod
    async def delete_post(self, post_id: int) -> bool:
        """The method removing post from the data storage.

        Args:
            post_id (int): The id of the post.

        Returns:
            bool: Result of the operation.
        """

    @abstractmethod
    async def update_post_rating(self, post_id: int, avg_rating: float, ratings_count: int) -> bool:
        """The method for updating post's rating statistics.

        Args:
            post_id (int): The id of the post.
            avg_rating (float): New average rating.
            ratings_count (int): Total number of ratings.

        Returns:
            bool: Success of the operation.
        """
