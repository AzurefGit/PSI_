"""A module containing DTO models for output airports."""


from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict

from core.domain.post import PostIn