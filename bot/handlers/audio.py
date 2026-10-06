import asyncio
import os
from aiogram import F, Router, types
from bot.keyboards.inline import get_tracks_keyboard
from bot.services.search import search_tracks
from shazamio import Shazam

router = Router()


@router.message(F.voice | F.audio)
async def recognize_audio_handler(message: types.Message):
  status_msg = await message.answer(
      "🎧 Слушаю аудиофрагмент и распознаю песню через Shazam..."
  )

  audio_obj = message.voice or message.audio
  file_id = audio_obj.file_id

  file = await message.bot.get_file(file_id)
  os.makedirs("downloads", exist_ok=True)
  temp_file_path = os.path.join("downloads", f"temp_{message.from_user.id}.ogg")

  await message.bot.download_file(file.file_path, destination=temp_file_path)

  try:
    shazam = Shazam()
    out = await shazam.recognize(temp_file_path)

    track = out.get("track")
    if not track:
      await status_msg.edit_text(
          "❌ Не удалось распознать песню по этому фрагменту."
      )
      return

    title = track.get("title", "Неизвестно")
    artist = track.get("subtitle", "Неизвестный исполнитель")
    full_query = f"{artist} - {title}"

    await status_msg.edit_text(
        f"🎯 Распознано: *{full_query}*\n🔍 Ищу песню",
        parse_mode="Markdown",
    )

    tracks = search_tracks(full_query, limit=5)

    if not tracks:
      await status_msg.edit_text(
          f"❌ Трек «{full_query}» распознан, но ничего не нашлось."
      )
      return

    keyboard = get_tracks_keyboard(tracks)
    await status_msg.edit_text(
        f"🎵 Распознано: *{full_query}*\nВыберите нужный вариант для скачивания:",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

  except Exception as e:
    await status_msg.edit_text(
        f"❌ Произошла ошибка при распознавании: `{e}`", parse_mode="Markdown"
    )

  finally:
    if os.path.exists(temp_file_path):
      os.remove(temp_file_path)