from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from aiochatgpt.apps.bot.callback_data.base_callback import Action
from aiochatgpt.apps.bot.callback_data.dialog import ChatModeCallback
from aiochatgpt.apps.bot.keyboards.common import chat_gpt_kbs, common_kbs
from aiochatgpt.db.models.dialog.chat_mode import ChatModeType, ChatMode

if TYPE_CHECKING:
    from aiochatgpt.locales.stubs.ru.stub import TranslatorRunner

router = Router()


@router.callback_query(ChatModeCallback.filter((F.action == Action.DELETE)))
async def delete_mode(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: ChatModeCallback,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.get_data()
    confirm: ChatMode | None = data.get("confirm_chat_mode")
    if confirm:
        await session.delete(confirm)
        await session.commit()
        await call.message.edit_text(
            l10n.chat_mode.deleted(name=confirm.name),
            reply_markup=common_kbs.custom_back_kb(
                l10n.button.back(),
                ChatModeCallback(
                    action=Action.ALL,
                    type=callback_data.type
                )
            )
        )
        await state.clear()
    else:
        chat_mode: ChatMode = await session.get(ChatMode, callback_data.id)
        await state.update_data(confirm_chat_mode=chat_mode)
        await call.answer(
            l10n.delete.confirm(),
        )
