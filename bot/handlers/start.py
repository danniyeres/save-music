from aiogram import Router, types
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! 🎵\n"
        "Отправь название песни, фрагмент текста или аудио"
    )
