"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.repositories.postdb import PostRepository
from infrastructure.services.post import PostService
from infrastructure.repositories.commentdb import CommentRepository
from infrastructure.services.comment import CommentService
from infrastructure.repositories.user import UserRepository
from infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    post_repository = Singleton(PostRepository)
    comment_repository = Singleton(CommentRepository)
    user_repository = Singleton(UserRepository)

    post_service = Factory(
        PostService,
        repository=post_repository
    )

    comment_service = Factory(
        CommentService,
        repository=comment_repository
    )

    user_service = Factory(
        UserService,
        repository=user_repository
    )
