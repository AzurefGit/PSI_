from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID4


class CommentIn(BaseModel):
    """Model representing comment's DTO attributes."""
    text: str
    rating: int
    nickname: str
    author_email: Optional[str]
    likes_count: int = 0
    parent_comment_id: Optional[int]


class CommentBroker(CommentIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Comment(CommentBroker):
    """Model representing comment's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
