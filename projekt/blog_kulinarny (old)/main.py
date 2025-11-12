"""Main module of the app"""

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler


app = FastAPI()
# app.include_router(post_router, prefix="/post")
# app.include_router(comment_router, prefix="/comment")

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