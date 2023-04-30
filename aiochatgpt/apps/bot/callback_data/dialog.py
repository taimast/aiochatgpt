from enum import StrEnum

from aiogram.filters.callback_data import CallbackData

from aiochatgpt.apps.bot.callback_data.base_callback import Action
from aiochatgpt.db.models.dialog.chat_mode import ChatModeType


class ChatAction(StrEnum):
    START_DIALOG = "start_dialog"


class ChatModeCallback(CallbackData, prefix="chat_mode"):
    id: int | None
    action: Action | ChatAction
    type: ChatModeType = ChatModeType.STANDARD


class DialogCallback(CallbackData, prefix="dialog"):
    id: int | None
    action: Action
    type: ChatModeType = ChatModeType.STANDARD
