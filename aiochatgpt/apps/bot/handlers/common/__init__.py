from aiogram import Router

from . import base, group, chatgpt

router = Router(name="common")
router.include_routers(
    base.router,
    group.router,
    chatgpt.router,
)
