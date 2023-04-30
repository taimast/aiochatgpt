from aiogram import Router

from . import dialog, custom


router = Router(name="chatgpt-modes")
router.include_routers(
    dialog.router,
    custom.router,
)
