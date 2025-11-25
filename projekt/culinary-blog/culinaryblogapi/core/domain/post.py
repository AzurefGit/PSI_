# from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID1


class PostIn(BaseModel):
    """Model representing post's DTO attributes."""
    body: str


class PostBroker(PostIn):
    """A broker class including user in the model."""
    user_id: UUID1


class Post(PostIn):
    """Model representing post's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
