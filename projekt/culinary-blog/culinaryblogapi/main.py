"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from culinaryblogapi.api.routers.post import router as post_router
from culinaryblogapi.api.routers.comment import router as comment_router
from culinaryblogapi.api.routers.rating import router as rating_router
from culinaryblogapi.api.routers.user import router as user_router
from culinaryblogapi.container import Container
from culinaryblogapi.db import database, init_db

container = Container()
container.wire(modules=[
    "culinaryblogapi.api.routers.post",
    "culinaryblogapi.api.routers.comment",
    "culinaryblogapi.api.routers.rating",
    "culinaryblogapi.api.routers.user",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post_router, prefix="/post")
app.include_router(comment_router, prefix="/comment")
app.include_router(rating_router, prefix="/rating")
app.include_router(user_router, prefix="")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
