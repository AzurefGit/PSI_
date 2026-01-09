"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from culinaryblogapi.infrastructure.repositories.postdb import PostRepository
from culinaryblogapi.infrastructure.services.post import PostService
from culinaryblogapi.infrastructure.repositories.commentdb import CommentRepository
from culinaryblogapi.infrastructure.services.comment import CommentService
from culinaryblogapi.infrastructure.repositories.ratingdb import RatingRepository
from culinaryblogapi.infrastructure.services.rating import RatingService
from culinaryblogapi.infrastructure.repositories.bookmarkdb import BookmarkRepository
from culinaryblogapi.infrastructure.services.bookmark import BookmarkService
from culinaryblogapi.infrastructure.repositories.user import UserRepository
from culinaryblogapi.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    post_repository = Singleton(PostRepository)
    comment_repository = Singleton(CommentRepository)
    rating_repository = Singleton(RatingRepository)
    bookmark_repository = Singleton(BookmarkRepository)
    user_repository = Singleton(UserRepository)
    
    post_service = Factory(
        PostService,
        repository=post_repository
    )

    comment_service = Factory(
        CommentService,
        repository=comment_repository
    )

    rating_service = Factory(
        RatingService,
        repository=rating_repository
    )

    bookmark_service = Factory(
        BookmarkService,
        repository=bookmark_repository
    )

    user_service = Factory(
        UserService,
        repository=user_repository
    )
