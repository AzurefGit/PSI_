import aiohttp
import random

from typing import Iterable

from core.domain.post import PostRecord
from core.repositories.ipost_repository import IPostRepository
from utils import consts


class PostRepository(IPostRepository):
    async def get_posts(self) -> Iterable[PostRecord] | None:
        all_params = await self._get_params()
        parsed_params = await self._parse_params(all_params)
        return parsed_params

    async def auto_clean(self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        filtered_posts = []
        for post in posts:
            if post.lastUsage < consts.N:
                filtered_posts.append(post)
        return filtered_posts

    async def filter_posts_by_text(self, posts: Iterable[PostRecord], text_fragment: str) -> Iterable[PostRecord] | None:
        filtered_posts = []
        for post in posts:
            if text_fragment.lower() in post.body.lower():
                filtered_posts.append(post)
        return filtered_posts

    async def sort_posts_by_time (self, posts: Iterable[PostRecord]) -> Iterable[PostRecord] | None:
        return sorted(posts, key=lambda post: post.lastUsage)

    async def _get_params(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POSTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()


    async def _parse_params(self, params: Iterable[dict]) -> Iterable[PostRecord]:
        return [PostRecord(userId=record.get("userId"), id=record.get("id"), title=record.get("title"), body=record.get("body"), lastUsage=random.randint(1,100)) for record in params]
