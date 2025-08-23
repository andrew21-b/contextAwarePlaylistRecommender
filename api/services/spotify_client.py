import requests
from typing import List
from api.context.config import settings


class SpotifyClient:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.access_token = None

        self.authenticate()

    def authenticate(self):
        auth_url = "https://accounts.spotify.com/api/token"
        res = requests.post(
            auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        print(f"Client ID: {self.client_id}, Client Secret: {self.client_secret}")
        res.raise_for_status()
        self.access_token = res.json()["access_token"]

    def get_auth_header(self):
        if not self.access_token:
            self.authenticate()
        return {"Authorization": f"Bearer {self.access_token}"}

    def search_track(self, query: str):
        url = "https://api.spotify.com/v1/search"
        params = {"q": query, "type": "track", "limit": 1}
        res = requests.get(url, headers=self.get_auth_header(), params=params)
        if res.status_code != 200 or not res.json()["tracks"]["items"]:
            return None
        return res.json()["tracks"]["items"][0]

    def audio_features(self, track_ids: List[str]):
        url = "https://api.spotify.com/v1/audio-features"
        params = {"ids": ",".join(track_ids)}
        res = requests.get(url, headers=self.get_auth_header(), params=params)
        res.raise_for_status()
        return res.json()["audio_features"]
