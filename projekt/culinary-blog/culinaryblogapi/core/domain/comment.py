from pydantic import BaseModel, ConfigDict, UUID4


class CommentIn(BaseModel):
    """Model representing comment's DTO attributes."""
    post_id: int
    text: str
    nickname: str


class CommentBroker(CommentIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Comment(CommentBroker):
    """Model representing comment's attributes in the database."""
    id: int
    likes: int = 0
    dislikes: int = 0

    model_config = ConfigDict(from_attributes=True, extra="ignore")
