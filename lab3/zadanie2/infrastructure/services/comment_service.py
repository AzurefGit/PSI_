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

    async def filter_comments(self, text_fragment: str) -> Iterable[CommentRecord] | None:
        return await self.repository.filter_comments(text_fragment)
