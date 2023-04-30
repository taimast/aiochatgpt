from typing import Sequence, TypeVar

from sqlalchemy import select, ChunkedIteratorResult, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .mixin import BaseQuery
# todo L1 TODO 18.04.2023 17:00 taima: Use func from sqlalchemy_utils. get_tables is not used

T = TypeVar("T", bound='Base')


class Base(DeclarativeBase, BaseQuery):
    """
    Base class for all models
    """