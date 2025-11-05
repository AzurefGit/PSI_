from dependency_injector.wiring import Provide

import asyncio

from container import Container
from infrastructure.services.ipost_service import IPostService
from infrastructure.services.icomment_service import ICommentService


async def main(
        post_service: IPostService = Provide[Container.post_service],
        comment_service: ICommentService = Provide[Container.comment_service]) -> None:

    # Clean posts sorting and searching
    posts = await post_service.get_posts()
    cleaned_posts = await post_service.auto_clean(posts)
    print(cleaned_posts)
    print('\n')
    sorted_posts = await post_service.sort_posts_by_time(cleaned_posts)
    print(sorted_posts)
    searched_posts = await post_service.filter_posts_by_text(posts=sorted_posts, text_fragment="doloribus")
    print(searched_posts)

    # Clean comments sorting and searching
    # comments = await comment_service.get_comments()
    # cleaned_comments = await comment_service.auto_clean(comments)
    # print(cleaned_comments)
    # print('\n')
    # sorted_comments = await comment_service.sort_comments_by_time(cleaned_comments)
    # print(sorted_comments)
    # searched_comments = await comment_service.filter_comments_by_text(comments=sorted_comments,text_fragment="doloribus")
    # print(searched_comments)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
