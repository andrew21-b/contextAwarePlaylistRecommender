import random
from api.services.context_rules_service import pick_playlist
from api.services.lastfm_client import get_similar_tracks


def recommend_for_context(context: dict, playlists: dict) -> dict:
    base_playlist = pick_playlist(context, playlists)
    seed_track = random.choice(base_playlist["tracks"])
    artist, title = seed_track.split(" - ")

    recommendations = get_similar_tracks(artist, title, limit=5)

    return {
        "context": context,
        "base_playlist": base_playlist["name"],
        "seed_track": seed_track,
        "recommendations": recommendations,
    }
