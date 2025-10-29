from abc import ABC
from typing import Iterable

from domains.post import PostRecord, CommentRecord


class IPostRepository(ABC):
    async def get_posts(self) -> Iterable[PostRecord] | None:
        pass

    async def get_comments(self) -> Iterable[CommentRecord] | None:
        pass

    async def filter_posts(self, text_fragment: str) -> Iterable[PostRecord] | None:
        pass

