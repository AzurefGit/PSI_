"""Module containing comment repository implementation."""

from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict


class CommentDTO(BaseModel):
    id: int
    post_id: int
    text: str
    nickname: str
    likes: int = 0
    dislikes: int = 0
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
            post_id=record_dict.get("post_id"),
            text=record_dict.get("text"),
            nickname=record_dict.get("nickname"),
            likes=record_dict.get("likes_count"),
            dislikes=record_dict.get("dislikes"),
            user_id=record_dict.get("user_id")
        )
