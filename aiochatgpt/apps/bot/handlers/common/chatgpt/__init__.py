from aiogram import Router

from . import base, modes

router = Router(name="chatgpt")
router.include_routers(
    base.router,
    modes.router,
)
