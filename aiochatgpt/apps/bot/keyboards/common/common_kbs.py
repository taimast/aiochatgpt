from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils import markdown as md
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from ...callback_data.base_callback import Action
from ...callback_data.dialog import ChatModeCallback
from .....db.models.dialog.chat_mode import ChatModeType

IKB = InlineKeyboardButton
KB = KeyboardButton
md = md
if TYPE_CHECKING:
    from .....locales.stubs.ru.stub import TranslatorRunner


def start(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=l10n.button.standard_modes(),
        callback_data=ChatModeCallback(action=Action.ALL, type=ChatModeType.STANDARD)
    )
    builder.button(
        text=l10n.button.advanced_modes(),
        callback_data=ChatModeCallback(action=Action.ALL, type=ChatModeType.ADVANCED)
    )
    builder.button(
        text=l10n.button.custom_modes(),
        callback_data=ChatModeCallback(action=Action.ALL, type=ChatModeType.CUSTOM)
    )
    builder.adjust(1)
    return builder.as_markup()


def custom_back(callback_data: str | CallbackData = "start") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="« Назад", callback_data=callback_data)
    return builder.as_markup()


def custom_back_kb(text: str = "« Назад", cd: str | CallbackData = "start") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=text, callback_data=cd)
    return builder.as_markup()


def inline_button(text: str, cd: CallbackData) -> InlineKeyboardButton:
    return IKB(text=text, callback_data=cd.pack())


def custom_back_inline_button(text: str = "« Назад", cd: str | CallbackData = "start") -> InlineKeyboardButton:
    if not isinstance(cd, str):
        cd = cd.pack()
    return IKB(text=text, callback_data=cd)


def custom_reply_kb(text: str = "« Назад") -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=text)
    return builder.as_markup(resize_keyboard=True)


def reply_back_button(l10n: TranslatorRunner) -> KeyboardButton:
    return KeyboardButton(text=l10n.button.back())


def reply_back() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="« Назад")
    return builder.as_markup(resize_keyboard=True)
