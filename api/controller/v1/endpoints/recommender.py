from typing import Optional
from fastapi import APIRouter, Query
from api.schemas.playlist_response import PlaylistResponse
from api.services.playlist_generator_service import generate_mood_playlist


router = APIRouter()


@router.get("/", response_model=PlaylistResponse)
async def get_recommendations(
    time_of_day: Optional[str] = Query(
        None, description="Time of day (e.g. 06:00, 15:00:00, 18:00, 22:00:00)"
    ),
    calendar_event: Optional[str] = Query(
        None, description="Current or next calendar event (e.g. Meeting with Bob)"
    ),
    location: Optional[str] = Query(
        None, description="Current location (e.g., Home, Office, Park)"
    ),
    social_post: Optional[str] = Query(None, description="Recent social media post"),
):

    playlist = await generate_mood_playlist(
        time_of_day=time_of_day,
        calendar_event=calendar_event,
        location=location,
        social_post=social_post,
    )

    return PlaylistResponse(**playlist)
