"""Module containing comment repository implementation."""


from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict


class CommentDTO(BaseModel):
    id: int
    text: str
    rating: int
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CommentDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CommentDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            text=record_dict.get("text"),
            rating=record_dict.get("rating")
        )

