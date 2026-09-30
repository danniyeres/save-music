import os
import asyncio
from aiogram import F, Router, types
from aiogram.types import FSInputFile
from bot.keyboards.inline import get_tracks_keyboard
from bot.services.downloader import download_audio
from bot.services.search import search_tracks

router = Router()


@router.message
async def select_song_handler(message: types.Message):
  query = message.text
  status_msg = await message.answer(
      f"🔍 Ищу песню: *{query}*...", parse_mode="Markdown"
  )

  tracks = search_tracks(query, limit=5)

  if not tracks:
    await status_msg.edit_text("❌ Ничего не найдено.")
    return

  keyboard = get_tracks_keyboard(tracks)

  await status_msg.edit_text(
      "🎵 Выберите нужный трек:",
      reply_markup=keyboard,
  )


@router.callback_query(F.data.startswith("dl_"))
async def download_selected_song(callback: types.CallbackQuery):
  url = callback.data.replace("dl_", "", 1)

  await callback.message.edit_text(
      "⏳ Скачиваю и конвертирую трек в MP3..."
  )

  try:
    loop = asyncio.get_running_loop()
    mp3_file_path = await loop.run_in_executor(
        None, download_audio, url
    )

    if not os.path.exists(mp3_file_path):
      await callback.message.edit_text(
          "❌ Не удалось скачать этот трек."
      )
      return

    await callback.message.edit_text("📤 Загружаю аудио в Telegram...")

    audio_file = FSInputFile(mp3_file_path)
    await callback.message.answer_audio(
        audio=audio_file
    )

    os.remove(mp3_file_path)
    await callback.message.delete()

  except Exception as e:
    await callback.message.edit_text(
        f"❌ Произошла ошибка при скачивании: `{e}`", parse_mode="Markdown"
    )