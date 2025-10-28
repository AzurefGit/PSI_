import aiohttp
import json

from typing import Iterable

from domains.post import PostRecord
from repositories.ipost_repository import IPostRepository
from utils import consts


class PostRepository(IPostRepository):
    async def get_posts(self) -> Iterable[PostRecord] | None:
        all_params = await self._get_params()
        parsed_params = await self._parse_params(all_params)
        return parsed_params

    async def filter_posts(self, text_fragment: str) -> Iterable[PostRecord] | None:
        posts = await self.get_posts()
        filtered_posts = []
        for post in posts:
            if text_fragment.lower() in post.title.lower():
                filtered_posts.append(post)
        return filtered_posts

    async def json_post(self) -> str:
        posts = await self.get_posts()
        json_post = []
        for post in posts:
            json_post.append({
                "userId": post.userId,
                "id": post.id,
                "title": post.title,
                "body": post.body
            })
        return json.dumps(json_post)

    async def _get_params(self) -> Iterable[dict] | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(consts.API_POSTS_URL) as response:
                if response.status != 200:
                    return None

                return await response.json()

    async def _parse_params(self, params: Iterable[dict]) -> Iterable[PostRecord]:
        return [PostRecord(userId=record.get("userId"), id=record.get("id"), title=record.get("title"), body=record.get("body")) for record in
                params]