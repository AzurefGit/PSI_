from abc import ABC
from typing import Iterable
from core.domain.comment import CommentRecord


class ICommentService(ABC):
    async def get_comments(self) -> Iterable[CommentRecord] | None:
        pass

    async def auto_clean(self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        pass

    async def filter_comments_by_text(self, comments: Iterable[CommentRecord], text_fragment: str) -> Iterable[CommentRecord] | None:
        pass

    async def sort_comments_by_time(self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        pass
