"""Module containing comment repository implementation."""
from typing import Optional

from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict


class PostDTO(BaseModel):
    id: int
    title: str
    body: str
    description: Optional[str]
    cook_time_minutes: Optional[int]
    tags: Optional[str]
    avg_rating: float
    ratings_count: int
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "PostDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            PostDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            body=record_dict.get("body"),
            description=record_dict.get("description"),
            cook_time_minutes=record_dict.get("cook_time_minutes"),
            tags=record_dict.get("tags"),
            avg_rating=record_dict.get("avg_rating"),
            ratings_count=record_dict.get("ratings_count"),
            user_id=record_dict.get("user_id")
        )
