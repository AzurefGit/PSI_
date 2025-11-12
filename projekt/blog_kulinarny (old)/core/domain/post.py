# from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostIn(BaseModel):
    """Model representing post's DTO attributes."""
    post_id: int
    body: str


class Post(PostIn):
    """Model representing post's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
