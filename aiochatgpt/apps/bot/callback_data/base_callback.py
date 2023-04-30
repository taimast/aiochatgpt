from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    GET = "get"
    CREATE = "create"
    DELETE = "delete"
    UPDATE = "update"
    ALL = "all"
    MENU = "menu"
    START = "start"
    STOP = "stop"


class UserCallback(CallbackData, prefix="user"):
    id: int
    action: Action
