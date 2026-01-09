from pydantic import BaseModel, ConfigDict, UUID4, Field


class RatingIn(BaseModel):
    """Model for user rating a post."""
    post_id: int
    rating: int = Field(ge=1, le=5, description="The rating of the post.")


class RatingBroker(RatingIn):
    """A broker class including user."""
    user_id: UUID4


class Rating(RatingIn):
    """Model representing rating's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")