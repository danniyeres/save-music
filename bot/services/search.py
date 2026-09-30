from yt_dlp import YoutubeDL


def search_tracks(query: str, limit: int = 5) -> list:

    ydl_opts = {
        'default_search': f'ytsearch{limit}',
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get('entries', [])