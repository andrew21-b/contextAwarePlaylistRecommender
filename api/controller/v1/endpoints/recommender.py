import json
from fastapi import APIRouter
from api.services.recommender_service import recommend_for_context


router = APIRouter()

with open("data/spotify_playlists.json") as f:
    playlists = json.load(f)["playlists"]


@router.get("/")
def get_recommendations(location: str, time_of_day: str, event: str):
    context = {"location": location, "time_of_day": time_of_day, "event": event}
    return recommend_for_context(context, playlists)
