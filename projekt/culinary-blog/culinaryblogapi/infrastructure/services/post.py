"""Module containing post service implementation."""
from typing import Iterable

from culinaryblogapi.core.domain.post import Post, PostBroker
from culinaryblogapi.core.repositories.ipost import IPostRepository
from culinaryblogapi.infrastructure.dto.postdto import PostDTO
from culinaryblogapi.infrastructure.services.ipost import IPostService


class PostService(IPostService):

    _repository: IPostRepository

    def __init__(self, repository: IPostRepository):
        """The initializer of the post service.

        Args:
            repository (IPostRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_posts(self) -> Iterable[Post]:
        """The method getting all posts from the repository.

        Returns:
            Iterable[Post]: All posts.
        """

        return await self._repository.get_all_posts()

    async def get_post_by_id(self, post_id: int) -> PostDTO | None:
        """The method getting post by given id.

        Args:
            post_id (int): The id of the post.

        Returns:
            PostDTO | None: The post details.
        """

        return await self._repository.get_post_by_id(post_id)

    async def get_by_title(self, text: str) -> Iterable[Post]:
        """The method getting posts by given title or by a part of it.
        Args:
            text (str): The title of the post.

        Returns:
            Iterable[Post]: The post collection.
        """

        return await self._repository.get_by_title(text)

    async def get_by_user(self, user_id: str) -> Iterable[Post]:
        """The method getting posts by user who added them.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Post]: The post collection.
        """

        return await self._repository.get_by_user(user_id)

    async def add_post(self, data: PostBroker) -> Post | None:
        """The method adding new post to the data storage.

        Args:
            data (Post): The details of the new post.

        Returns:
            Post | None: Full details of the new added post.
        """

        return await self._repository.add_post(data)

    async def update_post(self, post_id: int, data: PostBroker) -> Post | None:
        """The method updating post data in the data storage.

        Args:
            post_id (int): The id of the post.
            data (PostBroker): The details of the updated post.

        Returns:
            Post | None: The updated post details.
        """

        return await self._repository.update_post(post_id=post_id, data=data)

    async def delete_post(self, post_id: int) -> bool:
        """The method removing post from the data storage.

        Args:
            post_id (int): The id of the post.

        Returns:
            bool: Result of the operation.
        """

        return await self._repository.delete_post(post_id)

    async def update_post_rating(
        self,
        post_id: int,
        avg_rating: float,
        ratings_count: int
    ) -> bool:
        """The method for updating post's rating statistics.

        Args:
            post_id (int): The id of the post.
            avg_rating (float): The new average rating.
            ratings_count (int): The total number of ratings.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.update_post_rating(
            post_id,
            avg_rating,
            ratings_count
        )
