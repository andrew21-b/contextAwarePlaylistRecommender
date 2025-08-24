import json
import sys
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))
from api.services.spotify_client import SpotifyClient

data_dir = Path("data")


def audio_features(track_title: str):
    csv_path = data_dir / "MillionSongSubset.csv"
    df = pd.read_csv(csv_path)
    features = df[df["Title"] == track_title]
    if features.empty:
        print(f"No features found for TrackTitle: {track_title}")
        return None
    return features.iloc[0].to_dict()


def build_dataset():
    client = SpotifyClient()

    playlist_path = data_dir / "spotify_playlists.json"
    playlists = json.load(open(playlist_path))

    rows = []
    for playlist in playlists["playlists"]:
        for track in playlist["tracks"]:
            track_info = client.search_track(track)
            if not track_info:
                continue
            features = audio_features(track_info["name"])
            if not features:
                continue
            rows.append(
                {
                    "playlist": playlist["name"],
                    "track_id": track_info["id"],
                    "track_name": track_info["name"],
                    "artist": track_info["artists"][0]["name"],
                    "danceability": features.get("Danceability"),
                    "energy": features.get("Energy"),
                    "tempo": features.get("Tempo"),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(data_dir / "playlist_dataset.csv", index=False)
    print(f"Dataset saved at {data_dir/'playlist_dataset.csv'} with {len(df)} tracks.")
