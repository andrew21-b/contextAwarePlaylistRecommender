import json
import os
from datetime import datetime
from typing import Optional
from api.services.context_llm_service import infer_mood
from api.services.lastfm_client import get_tracks_by_mood


def load_spotify_playlists(file_path: str = "data/spotify_playlists.json") -> list:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)["playlists"]
    return []


def find_playlist_for_mood(mood: Optional[str], playlists: list) -> Optional[list]:
    for playlist in playlists:
        if mood and mood.lower() in playlist["name"].lower():
            return playlist["tracks"]
    return None


def normalize_time(time: Optional[str]) -> Optional[str]:
    if time is None:
        return None

    try:
        dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        normalized_time = dt.strftime("%H:%M")
    except ValueError:
        try:
            dt = datetime.strptime(time, "%H:%M")
            normalized_time = dt.strftime("%H:%M")
        except ValueError:
            raise ValueError(f"Unrecognized time format: {time}")

    match normalized_time:
        case _ if normalized_time < "11:59":
            return "morning"
        case _ if normalized_time >= "12:00" and normalized_time < "17:00":
            return "afternoon"
        case _ if normalized_time >= "17:00" and normalized_time < "20:00":
            return "evening"
        case _:
            return "night"


async def extend_playlist_with_tracks(
    max_tracks: int, mood: Optional[str], playlist: list
):
    needed = max_tracks - len(playlist)
    extra_tracks = await get_tracks_by_mood(mood, limit=needed)
    playlist.extend(extra_tracks)


async def generate_mood_playlist(
    time_of_day=None,
    calendar_event=None,
    location=None,
    social_post=None,
    max_tracks=10,
):
    playlists = load_spotify_playlists()

    mood = await infer_mood(
        normalize_time(time_of_day), calendar_event, location, social_post, playlists
    )

    local_tracks = find_playlist_for_mood(mood, playlists)

    if local_tracks:
        playlist = local_tracks[:max_tracks]

        if len(playlist) < max_tracks:
            await extend_playlist_with_tracks(max_tracks, mood, playlist)

        return {
            "mood": mood,
            "playlist": playlist,
            "source": "local+lastfm" if len(playlist) > len(local_tracks) else "local",
        }
    else:
        api_tracks = await get_tracks_by_mood(mood, limit=max_tracks)
        return {"mood": mood, "playlist": api_tracks, "source": "lastfm"}
