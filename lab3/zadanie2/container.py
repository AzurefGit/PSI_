from dependency_injector import containers, providers

from repositories.post_repository import PostRepository
from services.post_service import PostService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    repository = providers.Singleton(
        PostRepository,
    )

    service = providers.Factory(
        PostService,
        repository=repository,
    )
