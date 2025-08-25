import requests
from api.context.config import settings


def get_similar_tracks(artist: str, track: str, limit: int = 5) -> list[str]:
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getsimilar",
        "artist": artist,
        "track": track,
        "api_key": settings.LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "similartracks" in data:
        return [
            f"{t['artist']['name']} - {t['name']}"
            for t in data["similartracks"]["track"]
        ]
    return []


def get_tracks_by_mood(mood: str, limit: int = 10) -> list[str]:
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "tag.getTopTracks",
        "tag": mood,
        "api_key": settings.LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
    }
    response = requests.get(url, params=params)
    data = response.json()

    tracks = []
    if "tracks" in data and "track" in data["tracks"]:
        for track in data["tracks"]["track"]:
            tracks.append(f"{track['artist']['name']} - {track['name']}")
    return tracks
