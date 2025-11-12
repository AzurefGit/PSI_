"""A module containing continent endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from container import Container
from core.domain.post import Post, PostIn