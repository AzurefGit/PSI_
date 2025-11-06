from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentIn(BaseModel):
    """Model representing comment's DTO attributes."""
    comment_id: int
    text: str
    rating: int

class Comment(CommentIn):
    """Model representing comment's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
