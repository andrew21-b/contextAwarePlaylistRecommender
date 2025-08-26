from typing import List
from pydantic import BaseModel


class PlaylistResponse(BaseModel):
    mood: str
    playlist: List[str]
    source: str
