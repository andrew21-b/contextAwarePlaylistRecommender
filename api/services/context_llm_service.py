from typing import Optional
from openai import OpenAI
from api.context.config import settings
from api.services.context_rules_service import pick_playlist

client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def infer_mood(
    time_of_day: Optional[str],
    calendar_event: Optional[str],
    location: Optional[str],
    social_post: Optional[str],
    playlists: Optional[list],
) -> Optional[str]:
    prompt = f"""
    You are a music expert. I will give you some context about a user.
    Your task: Return a single Last.fm tag (genre, mood, or category)
    that best matches the situation.

    Context:
    Location: {location}
    Time of day: {time_of_day}
    Event: {calendar_event}
    social post: {social_post}

    Only return one tag, lowercase, e.g., "indie rock", "chillout", "dance".
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )
        mood = response.choices[0].message.content
        if mood != None:
            print(f"Inferred mood: {mood.strip().lower()}")
            return mood.strip().lower()
    except Exception:
        return pick_playlist(
            {
                "event": calendar_event,
                "location": location,
                "time_of_day": time_of_day,
                "social_post": social_post,
            },
            playlists,
        )
