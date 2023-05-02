from aiogram import Router

from . import base,dialog, custom


router = Router(name="chatgpt-modes")
router.include_routers(
    base.router,
    dialog.router,
    custom.router,
)
