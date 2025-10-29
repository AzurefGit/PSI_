from re import search

from dependency_injector.wiring import Provide

import asyncio
import json

from container import Container
from services.ipost_service import IPostService


async def main(service: IPostService = Provide[Container.service]) -> None:
    posts = await service.get_posts()

    searched_post = await service.filter_posts(text_fragment="ea molestias quasi exercitationem")

    print(posts)
    # print(searched_post)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
