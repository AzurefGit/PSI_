from dataclasses import dataclass


@dataclass
class CommentRecord:
    postId: int
    id: int
    name: str
    email: str
    body: str
