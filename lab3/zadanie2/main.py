from dependency_injector.wiring import Provide

import asyncio

from container import Container
from infrastructure.services.ipost_service import IPostService
from infrastructure.services.icomment_service import ICommentService


async def main(
        post_service: IPostService = Provide[Container.post_service],
        comment_service: ICommentService = Provide[Container.comment_service]) -> None:

    posts = await post_service.get_posts()
    print(posts)
    #
    # comments = await comment_service.get_comments()
    # print(comments)

    # searched_posts = await post_service.filter_posts(text_fragment="ea molestias quasi exercitationem")
    # searched_comments = await comment_service.filter_comments(text_fragment="doloribus")
    # print(searched_posts)




if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
