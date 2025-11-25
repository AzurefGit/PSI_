from typing import Optional

from pydantic import BaseModel, ConfigDict

from core.domain.post import PostIn


class CommentIn(BaseModel):
    """Model representing comment's DTO attributes."""
    post_id: int
    text: str
    rating: int


class Comment(CommentIn):
    """Model representing comment's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
