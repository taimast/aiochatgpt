from __future__ import annotations

import typing

import tiktoken
from loguru import logger
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.attributes import flag_modified

from .message import Message, Role
from ..base import Base

if typing.TYPE_CHECKING:
    from ..user import User
    from .chat_mode import ChatMode


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # logger.warning("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # logger.warning("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


class Dialog(Base):
    __tablename__ = "dialogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    messages: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    chat_mode_id: Mapped[int] = mapped_column(ForeignKey("chat_modes.id"))
    chat_mode: Mapped[ChatMode] = relationship(back_populates="dialogs")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="dialogs")

    def num_tokens(self, model="gpt-3.5-turbo"):
        return num_tokens_from_messages(self.messages, model=model)

    async def save(self, session: AsyncSession):
        flag_modified(self, "messages")
        await session.commit()

    def iter_messages(self, reverse=False, limit=None):
        """Iterate over messages in the dialog."""
        messages = self.messages if not reverse else reversed(self.messages)
        if limit is not None:
            messages = messages[:limit]
        for message in messages:
            yield Message.from_dict(message)

    def add_message(self, message: Message):
        """Add a message to the dialog."""
        self.messages.append(message.to_dict())
        flag_modified(self, "messages")

    def add_system_message(self, text: str):
        """Add a system message to the dialog."""
        self.add_message(Message(role=Role.SYSTEM, content=text))

    def add_user_message(self, text: str):
        """Add a user message to the dialog."""
        self.add_message(Message(role=Role.USER, content=text))

    def add_assistant_message(self, text: str):
        """Add an assistant message to the dialog."""
        self.add_message(Message(role=Role.ASSISTANT, content=text))
