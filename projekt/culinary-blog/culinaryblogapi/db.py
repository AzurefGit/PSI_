"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)


from culinaryblogapi.config import config


metadata = sqlalchemy.MetaData()

posts_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("cook_time_minutes", sqlalchemy.Integer),
    sqlalchemy.Column("tags", sqlalchemy.String),
    sqlalchemy.Column("avg_rating", sqlalchemy.Float, default=0.0),
    sqlalchemy.Column("ratings_count", sqlalchemy.Integer, default=0),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False
    )
)

comments_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("nickname", sqlalchemy.String),
    sqlalchemy.Column("likes", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("dislikes", sqlalchemy.Integer, default=0),
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("posts.id"),
        nullable=False
    ),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False
    )
)

ratings_table = sqlalchemy.Table(
    "ratings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("posts.id"),
        nullable=False
    ),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False
    )
)

bookmarks_table = sqlalchemy.Table(
    "bookmarks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("posts.id"),
        nullable=False
    ),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False
    )
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the database.

    Args:
        retries (int, optional): Number of retries of connect to database.
            Defaults to 5.
        delay (int, optional): Delay of connect do database. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to database after several retries.")
