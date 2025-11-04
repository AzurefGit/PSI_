from typing import Iterable

from core.domain.comment import CommentRecord
from infrastructure.repositories.comment_repository import ICommentRepository
from infrastructure.services.icomment_service import ICommentService


class CommentService(ICommentService):
    repository: ICommentRepository

    def __init__(self, repository: ICommentRepository) -> None:
        self.repository = repository

    async def get_comments(self) -> Iterable[CommentRecord]:
        return await self.repository.get_comments()

    async def auto_clean(self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        return await self.repository.auto_clean(comments)

    async def filter_comments_by_text(self, comments: Iterable[CommentRecord], text_fragment: str) -> Iterable[CommentRecord] | None:
        return await self.repository.filter_comments_by_text(comments, text_fragment)

    async def sort_comments_by_time(self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        return await self.repository.sort_comments_by_time(comments)