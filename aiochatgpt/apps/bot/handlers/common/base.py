from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from aiochatgpt.apps.bot.commands.bot_commands import BaseCommands
from aiochatgpt.apps.bot.keyboards.common import common_kbs

if TYPE_CHECKING:
    from aiochatgpt.locales.stubs.ru.stub import TranslatorRunner

router = Router()


@router.message(Command(BaseCommands.START))
@router.message(Text(startswith="«"))
@router.callback_query(Text("start"))
async def start(
        message: types.Message | types.CallbackQuery,
        l10n: TranslatorRunner,
        state: FSMContext
):
    await state.clear()
    if isinstance(message, types.CallbackQuery):
        message = message.message
        method = message.edit_text
    else:
        method = message.answer
    await method(l10n.start(), reply_markup=common_kbs.start(l10n))
