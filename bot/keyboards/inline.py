from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_tracks_keyboard(tracks: list):

    builder = InlineKeyboardBuilder()

    for i, track in enumerate(tracks):
        title = track.get('title', 'no title')
        short_title = title[:40] + "..." if len(title) > 40 else title

        url = track.get('webpage_url')

        builder.button(
            text=f"{i + 1}. {short_title}",
            callback_data=f"dl_{url}"
        )

    builder.adjust(1)
    return builder.as_markup()