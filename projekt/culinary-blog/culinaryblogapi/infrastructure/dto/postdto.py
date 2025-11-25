"""A module containing DTO models for output airports."""


from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from core.domain.post import Post



class PostDTO(BaseModel):
    """Model representing post's DTO attributes."""
    id: int
    body: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )
