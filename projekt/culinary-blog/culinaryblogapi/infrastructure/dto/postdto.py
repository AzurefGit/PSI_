"""Module containing comment repository implementation."""
from typing import Optional, Iterable

from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict

# from culinaryblogapi.core.domain.comment import Comment
from culinaryblogapi.infrastructure.dto.commentdto import CommentDTO

class PostDTO(BaseModel):
    id: int
    title: str
    body: str
    description: Optional[str]
    recipe_ingredients: Iterable[str]
    recipe_instructions: Iterable[str]
    cook_time_minutes: Optional[int]
    tags: Optional[Iterable[str]]
    image_url: Optional[str]
    # comments_section: Iterable[Comment] = None
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
            CommentDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            body=record_dict.get("body"),
            description=record_dict.get("description"),
            recipe_ingredients=record_dict.get("recipe_ingredients"),
            recipe_instructions=record_dict.get("recipe_instructions"),
            cook_time_minutes=record_dict.get("cook_time_minutes"),
            tags=record_dict.get("tags"),
            image_url=record_dict.get("image_url"),
            # comment_section=Iterable[CommentDTO(
            #     id=record_dict.get("id_1"),
            # )],
            user_id=record_dict.get("user_id")
        )
