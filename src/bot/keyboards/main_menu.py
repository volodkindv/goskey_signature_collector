from aiogram import Bot
from aiogram.types import BotCommand

from ..lexicon.lexicon import LexiconCommands


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(
            command=f"/{command}",
            description=description,
        )
        for command, description in LexiconCommands.__dict__.items()
        if not command.startswith("_")
    ]
    await bot.set_my_commands(main_menu_commands)
