from typing import Optional, Iterable

from pydantic import BaseModel, ConfigDict, UUID4


class PostIn(BaseModel):
    """Model representing post's DTO attributes."""
    title: str
    body: str
    description: Optional[str]
    recipe_ingredients: Iterable[str]
    recipe_instructions: Iterable[str]
    cook_time_minutes: Optional[int]
    tags: Optional[Iterable[str]]
    image_url: Optional[str]


class PostBroker(PostIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Post(PostBroker):
    """Model representing post's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
