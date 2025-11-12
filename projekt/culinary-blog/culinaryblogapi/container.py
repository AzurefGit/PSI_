from dependency_injector import containers, providers

# from infrastructure.repositories.post_repository import PostRepository
# from infrastructure.services.post_service import PostService
# from infrastructure.repositories.comment_repository import CommentRepository
# from infrastructure.services.comment_service import CommentService



class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    post_repository = providers.Singleton(PostRepository)
    comment_repository = providers.Singleton(CommentRepository)

    post_service = providers.Factory(
        PostService,
        repository=post_repository
    )

    comment_service = providers.Factory(
        CommentService,
        repository=comment_repository
    )
