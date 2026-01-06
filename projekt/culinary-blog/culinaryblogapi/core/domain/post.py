from typing import Optional, List

from pydantic import BaseModel, ConfigDict, UUID4

# from culinaryblogapi.core.domain.comment import Comment


class PostIn(BaseModel):
    """Model representing post's DTO attributes."""
    title: str
    body: str
    description: Optional[str]
    recipe_ingredients: str
    recipe_instructions: str
    cook_time_minutes: Optional[int]
    tags: Optional[str]
    # comments_section: List[Comment] = None
    image_url: Optional[str]


class PostBroker(PostIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Post(PostBroker):
    """Model representing post's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
