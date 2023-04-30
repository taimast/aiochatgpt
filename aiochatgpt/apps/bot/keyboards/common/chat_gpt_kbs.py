from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils import markdown as md
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .common_kbs import custom_back_inline_button
from ...callback_data.base_callback import Action
from ...callback_data.dialog import ChatModeCallback, ChatAction, DialogCallback
from .....db.models.dialog.chat_mode import ChatModeType, ChatMode

IKB = InlineKeyboardButton
KB = KeyboardButton
md = md
if TYPE_CHECKING:
    from .....locales.stubs.ru.stub import TranslatorRunner


def custom_modes(modes: list[ChatMode], l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for mode in modes:
        builder.button(
            text=mode.name,
            callback_data=ChatModeCallback(action=Action.GET, type=ChatModeType.CUSTOM, id=mode.id)
        )

    builder.button(
        text=l10n.button.dialogs(),
        callback_data=DialogCallback(action=Action.ALL, type=ChatModeType.CUSTOM)
    )

    # Создать
    builder.button(
        text=l10n.custom_modes.button.create(),
        callback_data=ChatModeCallback(action=Action.CREATE, type=ChatModeType.CUSTOM)
    )
    builder.add(custom_back_inline_button())
    builder.adjust(1)
    return builder.as_markup()


def custom_mode(mode: ChatMode, l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=l10n.custom_mode.button.start(),
        callback_data=ChatModeCallback(action=ChatAction.START_DIALOG, type=ChatModeType.CUSTOM, id=mode.id)
    )

    builder.button(
        text=l10n.custom_mode.button.update(),
        callback_data=ChatModeCallback(action=Action.UPDATE, type=ChatModeType.CUSTOM, id=mode.id)
    )
    builder.button(
        text=l10n.custom_mode.button.delete(),
        callback_data=ChatModeCallback(action=Action.DELETE, type=ChatModeType.CUSTOM, id=mode.id)
    )
    builder.button(text=l10n.button.back(), callback_data=ChatModeCallback(action=Action.ALL, type=ChatModeType.CUSTOM))
    builder.adjust(1)
    return builder.as_markup()
