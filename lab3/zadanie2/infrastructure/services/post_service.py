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

    async def filter_posts(self, text_fragment: str) -> Iterable[PostRecord] | None:
        return await self.repository.filter_posts(text_fragment)
