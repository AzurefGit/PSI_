from typing import Iterable

from core.domain.post import PostRecord
from infrastructure.repositories.post_repository import IPostRepository
from infrastructure.services.ipost_service import IPostService


class PostService(IPostService):
    repository: IPostRepository

    def __init__(self, repository: IPostRepository) -> None:
        self.repository = repository

    async def get_posts(self) -> Iterable[PostRecord]:
        return await self.repository.get_posts()

    async def auto_clean(self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        return await self.repository.auto_clean(posts)

    async def filter_posts_by_text(self, posts: Iterable[PostRecord], text_fragment: str) -> Iterable[PostRecord] | None:
        return await self.repository.filter_posts_by_text(posts, text_fragment)

    async def sort_posts_by_time(self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        return await self.repository.sort_posts_by_time(posts)