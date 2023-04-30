from __future__ import annotations

import typing
from enum import StrEnum
from functools import partial

from aiogram import types
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .dialog import Dialog
from .message import Message, Role
from ..base import Base
from ..user import User

if typing.TYPE_CHECKING:
    pass


class ChatModeType(StrEnum):
    STANDARD = "standard"
    ADVANCED = "advanced"
    CUSTOM = "custom"


class ChatMode(Base):
    __tablename__ = "chat_modes"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[ChatModeType] = mapped_column()
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str | None] = mapped_column(String(1000))
    photo_id: Mapped[str | None] = mapped_column(String(100))
    prompt: Mapped[str] = mapped_column(String(5000))
    dialogs: Mapped[list[Dialog]] = relationship(back_populates="chat_mode")

    def create_dialog(self, session: AsyncSession, user: User, name: str | None = None) -> Dialog:
        """Create a dialog with this chat mode."""
        dialog = Dialog(
            chat_mode=self,
            name=name or self.name,
            user=user,
            messages=[Message(Role.SYSTEM, self.prompt).to_dict()],
        )
        session.add(dialog)
        return dialog

    def get_answer_method(self, message: types.Message):
        if self.photo_id:
            return partial(message.answer_photo, self.photo_id)
        return message.answer
