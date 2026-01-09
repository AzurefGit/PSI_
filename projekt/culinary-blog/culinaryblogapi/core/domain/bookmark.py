from pydantic import BaseModel, UUID4, ConfigDict


class BookmarkIn(BaseModel):
    """A class representing a bookmark's DTO attributes."""
    user_id: UUID4
    post_id: int


class Bookmark(BookmarkIn):
    """A class representing bookmark's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
