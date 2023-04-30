from aiochatgpt.apps.chatgpt.group_manager import GPTGroupManager
from aiochatgpt.config import Settings


def setup_gpt_group_manager(
        settings: Settings,
) -> GPTGroupManager:
    gpt_group_manager = GPTGroupManager()

    for model in settings.chatgpt.models:
        gpt_group_manager.add_model(model)

    return gpt_group_manager
