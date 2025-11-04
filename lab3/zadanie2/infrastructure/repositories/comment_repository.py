import random

import aiohttp


from typing import Iterable

from core.domain.comment import CommentRecord
from core.repositories.icomment_repository import ICommentRepository
from utils import consts


class CommentRepository(ICommentRepository):
    async def get_comments(self) -> Iterable[CommentRecord] | None:
        all_params = await self._get_params()
        parsed_params = await self._parse_params(all_params)
        return parsed_params

    async def auto_clean(self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        filtered_comments = []
        for comment in comments:
            if comment.lastUsage < consts.N:
                filtered_comments.append(comment)
        return filtered_comments

    async def filter_comments_by_text(self, comments: Iterable[CommentRecord], text_fragment: str) -> Iterable[CommentRecord] | None:
        filtered_comments = []
        for comment in comments:
            if text_fragment.lower() in comment.body.lower():
                filtered_comments.append(comment)
        return filtered_comments

    async def sort_comments_by_time (self, comments: Iterable[CommentRecord]) -> Iterable[CommentRecord] | None:
        return sorted(comments, key=lambda comment: comment.lastUsage)

    async def _get_params(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_COMMENTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()


    async def _parse_params(self, params: Iterable[dict]) -> Iterable[CommentRecord]:
        return [CommentRecord(postId=record.get("postId"), id=record.get("id"), name=record.get("name"), email=record.get("email"), body=record.get("body"), lastUsage=random.randint(1, 100)) for record in params]