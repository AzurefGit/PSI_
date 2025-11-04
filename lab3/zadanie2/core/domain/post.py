from dataclasses import dataclass


@dataclass
class PostRecord:
    userId: int
    id: int
    title: str
    body: str
    lastUsage: int