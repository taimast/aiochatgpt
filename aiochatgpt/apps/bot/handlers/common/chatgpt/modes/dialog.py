from __future__ import annotations

import asyncio
from functools import cache, partial
from typing import TYPE_CHECKING

from aiogram import Router, F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from aiochatgpt.apps.bot.callback_data.base_callback import Action
from aiochatgpt.apps.bot.callback_data.dialog import ChatModeCallback, ChatAction, DialogCallback
from aiochatgpt.apps.bot.keyboards.common import common_kbs, chat_gpt_kbs
from aiochatgpt.apps.bot.keyboards.common.common_kbs import md
from aiochatgpt.apps.chatgpt.group_manager import GPTGroupManager
from aiochatgpt.apps.chatgpt.model import GPTModel
from aiochatgpt.apps.chatgpt.sender import QueueSender
from aiochatgpt.db.models import User
from aiochatgpt.db.models.dialog import Message, Dialog
from aiochatgpt.db.models.dialog.chat_mode import ChatMode

if TYPE_CHECKING:
    from aiochatgpt.locales.stubs.ru.stub import TranslatorRunner

router = Router()


@cache
def get_locker(user_id):
    return asyncio.Lock()


@router.callback_query(ChatModeCallback.filter(F.action == ChatAction.START_DIALOG))
async def start_dialog(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: ChatModeCallback,
        l10n: TranslatorRunner,
        state: FSMContext
):
    await state.clear()
    chat_mode = await session.get(ChatMode, callback_data.id)
    await state.update_data(chat_mode=chat_mode)
    await call.message.answer(
        l10n.dialog.start(),
        reply_markup=common_kbs.custom_reply_kb(l10n.button.skip())
    )
    await state.set_state("dialog-name")


async def _transition_to_dialog(
        message: types.Message,
        dialog: Dialog,
        gpt_model: GPTModel,
        user: User,
        l10n: TranslatorRunner,
        state: FSMContext,
):
    used_tokens = dialog.num_tokens(user.gpt_model)
    max_tokens = gpt_model.max_tokens
    await message.answer(
        l10n.dialog.used_tokens(
            used_tokens=md.hcode(used_tokens),
            max_tokens=md.hcode(max_tokens)
        ),
        reply_markup=common_kbs.custom_back_kb(
            l10n.button.back(),
            ChatModeCallback(
                action=Action.GET,
                id=dialog.chat_mode_id,
                type=dialog.chat_mode.type
            )
        )
    )

    await state.set_state("dialog")
    await state.update_data(
        dialog=dialog,
        used_tokens=used_tokens,
        max_tokens=max_tokens
    )


@router.message(StateFilter("dialog-name"))
async def dialog_name(
        message: types.Message,
        session: AsyncSession,
        user: User,
        gpt_group_manager: GPTGroupManager,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.update_data(name=message.text)
    name: str = data["name"]
    chat_mode: ChatMode = data.get("chat_mode")
    if name.startswith("〰️"):
        name = chat_mode.name
    dialog = chat_mode.create_dialog(session, user, name)
    session.add(dialog)
    await session.commit()
    dialog_message = Message.from_dict(dialog.messages[0])
    gpt_model = gpt_group_manager.get_model(user.gpt_model)

    await message.answer(l10n.dialog.start.starting(
        name=name,
        mode=chat_mode.name,
        model=gpt_model.model
    ))
    await message.answer(dialog_message.pretty())
    await _transition_to_dialog(
        message,
        dialog,
        gpt_model,
        user,
        l10n,
        state
    )


@router.callback_query(DialogCallback.filter(F.action == Action.CONTINUE))
async def continue_dialog(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: DialogCallback,
        user: User,
        gpt_group_manager: GPTGroupManager,
        l10n: TranslatorRunner,
        state: FSMContext
):
    dialog: Dialog = await session.get(Dialog, callback_data.id)
    await state.update_data(dialog=dialog, chat_mode=dialog.chat_mode)
    gpt_model = gpt_group_manager.get_model(user.gpt_model)
    model = gpt_model.model
    await call.message.answer(l10n.dialog.start.starting(
        name=dialog.name,
        mode=dialog.chat_mode.name,
        model=model
    ))
    for message in dialog.iter_messages(reverse=True, limit=2):
        await call.message.answer(message.pretty())
        await asyncio.sleep(0.3)
    await _transition_to_dialog(
        call.message,
        dialog,
        gpt_model,
        user,
        l10n,
        state
    )


@router.message(StateFilter("dialog"))
async def dialog_message(
        message: types.Message,
        session: AsyncSession,
        user: User,
        gpt_group_manager: GPTGroupManager,
        l10n: TranslatorRunner,
        state: FSMContext
):
    lock = get_locker(user.id)
    if lock.locked():
        await message.answer(l10n.dialog.wait())
        return

    async with lock:
        data = await state.get_data()
        dialog: Dialog = data["dialog"]
        await session.merge(dialog)
        dialog.add_user_message(message.text)
        sm = await message.answer("...")
        rmk = common_kbs.custom_back_kb(
            l10n.dialog.button.stop(),
            DialogCallback(action=Action.STOP)
        )
        cb = partial(sm.edit_text, reply_markup=rmk)
        sender = QueueSender(cb, sleep=0.5)
        completion_task = asyncio.create_task(
            gpt_group_manager.stream_completion(
                user.gpt_model,
                dialog.messages,
                sender.send,
            )
        )
        await state.update_data(completion_task=completion_task)
        try:
            completion_text = await completion_task
        except asyncio.CancelledError:
            logger.info("Dialog cancelled")
            return
        dialog.add_assistant_message(completion_text)
        await session.commit()
        await sender.close()
        try:
            await sm.edit_text(
                completion_text,
                reply_markup=rmk,
                # reply_markup=common_kbs.custom_back_kb(
                #     l10n.button.back(),
                #     ChatModeCallback(
                #         action=Action.GET,
                #         id=dialog.chat_mode_id,
                #         type=dialog.chat_mode.type
                #     )
                # )

            )
        except TelegramBadRequest as e:
            if "Bad Request: message is not modified" in e.message:
                logger.info("Message is not modified")
            else:
                raise
        used_tokens = dialog.num_tokens(user.gpt_model)
        max_tokens = data["max_tokens"]
        await message.answer(
            l10n.dialog.used_tokens(
                used_tokens=md.hcode(used_tokens),
                max_tokens=md.hcode(max_tokens)
            )
        )


@router.callback_query(DialogCallback.filter(F.action == Action.STOP))
async def stop_dialog(
        call: types.CallbackQuery,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.get_data()
    chat_mode: ChatMode = data.get("chat_mode")
    dialog: Dialog = data.get("dialog")
    if not chat_mode:
        await call.message.answer(l10n.dialog.not_started())
        return
    completion_task: asyncio.Task = data["completion_task"]
    completion_task.cancel()
    await call.message.answer(
        l10n.dialog.stop(),
        reply_markup=common_kbs.custom_back_kb(
            l10n.button.back(),
            DialogCallback(
                action=Action.GET,
                id=dialog.id,
                type=dialog.chat_mode.type
            )
        )
    )
    await state.clear()


@router.callback_query(ChatModeCallback.filter(F.action == ChatAction.DIALOGS))
async def get_dialogs(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: ChatModeCallback,
        user: User,
        l10n: TranslatorRunner
):
    chat_mode: ChatMode = await session.get(ChatMode, callback_data.id)
    await session.refresh(chat_mode, ["dialogs"])
    dialogs = chat_mode.dialogs
    if not dialogs:
        await call.message.answer(l10n.dialog.no_dialogs(mode=chat_mode.name))
        return
    await call.message.edit_text(
        l10n.dialog.dialogs(mode=chat_mode.name),
        reply_markup=chat_gpt_kbs.dialogs(dialogs, l10n)
    )


@router.callback_query(DialogCallback.filter(F.action == Action.GET))
async def get_dialog(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: DialogCallback,
        gpt_group_manager: GPTGroupManager,
        user: User,
        l10n: TranslatorRunner
):
    dialog: Dialog = await session.get(Dialog, callback_data.id)
    model = gpt_group_manager.get_model(user.gpt_model)
    used_tokens = dialog.num_tokens(user.gpt_model)
    await call.message.edit_text(
        l10n.dialog.dialog(
            name=dialog.name,
            mode=dialog.chat_mode.name,
            model=user.gpt_model,
            used_tokens=md.hcode(used_tokens),
            max_tokens=md.hcode(model.max_tokens)
        ),
        reply_markup=chat_gpt_kbs.dialog(dialog, l10n)
    )


@router.callback_query(DialogCallback.filter(F.action == Action.DELETE))
async def delete_dialog(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: DialogCallback,
        l10n: TranslatorRunner,
        state: FSMContext
):
    data = await state.get_data()
    confirm: Dialog | None = data.get("confirm_dialog")
    if confirm:
        await session.delete(confirm)
        await session.commit()
        await call.message.edit_text(
            l10n.dialog.deleted(name=confirm.name),
            reply_markup=common_kbs.custom_back_kb(
                l10n.button.back(),
                ChatModeCallback(
                    action=Action.GET,
                    id=confirm.chat_mode_id,
                    type=confirm.chat_mode.type
                )
            )
        )
        await state.clear()
    else:
        dialog: Dialog = await session.get(Dialog, callback_data.id)
        await state.update_data(confirm_dialog=dialog)
        await call.answer(
            l10n.delete.confirm(),
        )
