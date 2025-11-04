from abc import ABC
from typing import Iterable

from core.domain.comment import CommentRecord

class ICommentRepository(ABC):
    async def get_comments(self) -> Iterable[CommentRecord] | None:
        pass

    async def filter_comments(self, text_fragment: str) -> Iterable[CommentRecord] | None:
        pass
