from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from aiochatgpt.apps.bot.commands.bot_commands import BaseCommands
from aiochatgpt.apps.chatgpt.group_manager import GPTGroupManager
from aiochatgpt.db.models import User

if TYPE_CHECKING:
    from aiochatgpt.locales.stubs.ru.stub import TranslatorRunner

router = Router()


@router.message(Command(BaseCommands.CHANGE_MODEL))
async def change_model(
        message: types.Message,
        user: User,
        session: AsyncSession,
        gpt_group_manager: GPTGroupManager,
        l10n: TranslatorRunner,
        state: FSMContext
):
    models = gpt_group_manager.get_model_names()
    for model in models:
        if model != user.gpt_model:
            user.gpt_model = model
            await session.commit()
            await message.answer(
                l10n.model_changed(model=model)
            )
            return
