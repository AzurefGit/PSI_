"""Module containing rating repository implementation."""

from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict


class RatingDTO(BaseModel):
    id: int
    post_id: int
    rating: int
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "RatingDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            RatingDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            post_id=record_dict.get("post_id"),
            rating=record_dict.get("rating"),
            user_id=record_dict.get("user_id")
        )
