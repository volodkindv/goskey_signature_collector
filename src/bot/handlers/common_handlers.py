from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from ..lexicon.lexicon import Lexicon

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    await message.answer(Lexicon.start, reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands="help"))
async def process_help_command(message: Message) -> None:
    await message.answer(Lexicon.help)
