from dataclasses import dataclass


@dataclass
class PostRecord:
    userId: int
    id: int
    title: str
    body: str


@dataclass
class CommentRecord:
    postId: int
    id: int
    name: str
    email: str
    body: str
