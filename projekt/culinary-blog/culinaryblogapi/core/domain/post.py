from typing import Optional
from pydantic import BaseModel, ConfigDict, UUID4


class PostIn(BaseModel):
    """Model representing post's DTO attributes."""
    title: str
    body: str
    description: Optional[str]
    cook_time_minutes: Optional[int]
    tags: Optional[str]


class PostBroker(PostIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Post(PostBroker):
    """Model representing post's attributes in the database."""
    id: int
    avg_rating: float
    ratings_count: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
