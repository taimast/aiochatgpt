from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from aiochatgpt.db.models import User


class UserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        session: AsyncSession = data["session"]
        logger.debug("Get user for User {}", user.id)
        db_user = await session.get(User, user.id)
        if not db_user:
            logger.info(f"Новый пользователь {user=}")
            db_user = User(**user.dict(include={c.key for c in User.__table__.columns}))
            session.add(db_user)
            await session.commit()

        data["user"] = db_user
        return await handler(event, data)
