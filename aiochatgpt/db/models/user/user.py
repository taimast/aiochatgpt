from __future__ import annotations

import datetime
from enum import StrEnum

from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from aiochatgpt.apps.chatgpt.model import GPTModelName
from .base import BaseUser
from ..dialog import Dialog


class Locale(StrEnum):
    """Language codes."""
    ENGLISH = 'en'
    RUSSIAN = 'ru'


class User(BaseUser):
    __tablename__ = 'users'
    language_code: Mapped[Locale | None] = mapped_column(default=Locale.RUSSIAN)
    gpt_model: Mapped[GPTModelName] = mapped_column(String(30), default=GPTModelName.GPT_3_5_TURBO)
    dialogs: Mapped[list[Dialog]] = relationship(back_populates='user')

    @classmethod
    async def today_count(cls, session: AsyncSession) -> int:
        result = await session.execute(
            select(cls).where(cls.created_at >= datetime.date.today()))
        return len(result.all())
