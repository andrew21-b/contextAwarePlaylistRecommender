from typing import Optional
from openai import OpenAI
from api.context.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def infer_mood(
    time_of_day: Optional[str],
    calendar_event: Optional[str],
    location: Optional[str],
    social_post: Optional[str],
) -> str:
    prompt = f"""
    You are a music mood assistant. Based on context, return ONE mood keyword.

    Location: {location}
    Time of day: {time_of_day}
    Event: {calendar_event}
    social post: {social_post}

    Examples:
    - Home at night → "chill"
    - Office during work hours → "focus"
    - Gym or running in morning → "energetic"
    - Dinner date → "romantic"

    Answer with only one word mood:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        return f"Mood is empty, Error occurred: {e}"

    mood = response.choices[0].message.content
    if mood != None:
        return mood.strip().lower()
    return "Mood is empty"
