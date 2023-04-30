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


class CreateCustomChatMode(StatesGroup):
    name = State()
    description = State()
    photo = State()
    prompt = State()


@router.callback_query(
    ChatModeCallback.filter(
        (F.action == Action.ALL) & (F.type == ChatModeType.CUSTOM)
    )
)
async def custom_mode(
        call: types.CallbackQuery,
        session: AsyncSession,
        l10n: TranslatorRunner,
        state: FSMContext
):
    await state.clear()
    modes = await ChatMode.filter(session, ChatMode.type == ChatModeType.CUSTOM)
    await call.message.edit_text(
        l10n.custom_modes(),
        reply_markup=chat_gpt_kbs.custom_modes(modes, l10n),
    )


@router.callback_query(
    ChatModeCallback.filter(
        (F.action == Action.GET) & (F.type == ChatModeType.CUSTOM)
    )
)
async def custom_mode_get(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: ChatModeCallback,
        l10n: TranslatorRunner,
        state: FSMContext
):
    await state.clear()

    mode = await session.get(ChatMode, callback_data.id)
    await call.message.edit_text(
        l10n.custom_mode(
            name=mode.name,
            description=mode.description,
            prompt=mode.prompt,
        ),
        reply_markup=chat_gpt_kbs.custom_mode(mode, l10n)
    )


@router.callback_query(
    ChatModeCallback.filter(
        (F.action == Action.CREATE) & (F.type == ChatModeType.CUSTOM)
    )
)
async def custom_mode_create(
        call: types.CallbackQuery,
        l10n: TranslatorRunner,
        state: FSMContext
):
    await call.message.edit_text(
        l10n.custom_mode.create(),
        reply_markup=common_kbs.custom_back_kb(l10n.button.back()),
    )
    await state.set_state(CreateCustomChatMode.name)


@router.message(CreateCustomChatMode.name)
async def custom_mode_create_name(
        message: types.Message,
        l10n: TranslatorRunner,
        state: FSMContext
):
    chat_mode = ChatMode(
        name=message.text,
        type=ChatModeType.CUSTOM
    )
    await state.update_data(chat_mode=chat_mode)
    await message.answer(
        l10n.custom_mode.create.description(name=chat_mode.name),
        reply_markup=common_kbs.custom_reply_kb(l10n.button.skip())
    )
    await state.set_state(CreateCustomChatMode.description)


@router.message(CreateCustomChatMode.description)
async def custom_mode_create_description(
        message: types.Message,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.get_data()
    chat_mode: ChatMode = data.get('chat_mode')
    if message.text.startswith("〰️"):
        chat_mode.description = "no description"
    else:
        chat_mode.description = message.text

    await message.answer(
        l10n.custom_mode.create.photo(
            name=chat_mode.name,
            description=chat_mode.description
        ),
        reply_markup=common_kbs.custom_reply_kb(l10n.button.skip())
    )
    await state.set_state(CreateCustomChatMode.photo)


@router.message(CreateCustomChatMode.photo)
async def custom_mode_create_photo(
        message: types.Message,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.get_data()
    chat_mode: ChatMode = data.get('chat_mode')
    if message.photo:
        chat_mode.photo_id = message.photo[-1].file_id
    method = chat_mode.get_answer_method(message)
    await method(
        l10n.custom_mode.create.prompt(
            name=chat_mode.name,
            description=chat_mode.description,
        ), reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CreateCustomChatMode.prompt)


@router.message(CreateCustomChatMode.prompt)
async def custom_mode_create_prompt(
        message: types.Message,
        l10n: TranslatorRunner,
        session: AsyncSession,
        state: FSMContext
):
    data = await state.get_data()
    chat_mode: ChatMode = data.get('chat_mode')
    chat_mode.prompt = message.text
    session.add(chat_mode)
    await session.commit()
    method = chat_mode.get_answer_method(message)
    await method(
        l10n.custom_mode.create.success(
            name=chat_mode.name,
            description=chat_mode.description,
            prompt=chat_mode.prompt,
        ), reply_markup=chat_gpt_kbs.custom_mode(chat_mode, l10n)
    )
    await state.clear()
