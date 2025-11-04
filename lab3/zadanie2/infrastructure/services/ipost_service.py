from abc import ABC
from typing import Iterable
from core.domain.post import PostRecord


class IPostService(ABC):
    async def get_posts(self) -> Iterable[PostRecord] | None:
        pass

    async def auto_clean(self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        pass

    async def filter_posts_by_text(self, posts: Iterable[PostRecord], text_fragment: str) -> Iterable[PostRecord] | None:
        pass

    async def sort_posts_by_time(self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        pass
