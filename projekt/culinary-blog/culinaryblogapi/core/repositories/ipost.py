from abc import ABC, abstractmethod
from typing import Iterable

from culinaryblogapi.core.domain.post import PostIn, Post


class IPostRepository(ABC):
    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> Post | None:
        """The abstract getting a post from the data storage.

        Args:
            post_id (int): The id of the post.

        Returns:
            post | None: The post data if exists.
        """

    @abstractmethod
    async def get_all_posts(self) -> Iterable[Post]:
        """The abstract getting all posts from the data storage.

        Returns:
            Iterable[Post]: The collection of the all posts.
        """

    @abstractmethod
    async def add_post(self, data: PostIn) -> None:
        """The abstract adding new post to the data storage.

        Args:
            data (PostIn): The attributes of the post.
        """

    @abstractmethod
    async def update_post(self, post_id: int, data: PostIn) -> Post | None:
        """The abstract updating post data in the data storage.

        Args:
            post_id (int): The post id.
            data (PostIn): The attributes of the post.

        Returns:
            Post | None: The updated post
        """

    @abstractmethod
    async def delete_post(self, post_id: int) -> bool:
        """The abstract updating removing post from the data storage.

        Args:
            post_id (int): The post id.

        Returns:
            bool: Success of the operation
        """
