import pytest
import json
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()
import api.services.playlist_generator_service as pgs


@pytest.fixture
def sample_playlists(tmp_path):
    playlists = [
        {"name": "Happy Morning", "tracks": ["track1", "track2", "track3"]},
        {"name": "Sad Night", "tracks": ["track4", "track5"]},
    ]
    file_path = tmp_path / "spotify_playlists.json"
    with open(file_path, "w") as f:
        json.dump({"playlists": playlists}, f)
    return str(file_path), playlists


def test_load_spotify_playlists_file_exists(sample_playlists):
    file_path, playlists = sample_playlists
    loaded = pgs.load_spotify_playlists(file_path)
    assert loaded == playlists


def test_load_spotify_playlists_file_not_exists(tmp_path):
    file_path = tmp_path / "nonexistent.json"
    loaded = pgs.load_spotify_playlists(str(file_path))
    assert loaded == []


def test_find_playlist_for_mood_found():
    playlists = [
        {"name": "Chill Vibes", "tracks": ["a", "b"]},
        {"name": "Energetic Mood", "tracks": ["c", "d"]},
    ]
    result = pgs.find_playlist_for_mood("energetic", playlists)
    assert result == ["c", "d"]


def test_find_playlist_for_mood_not_found():
    playlists = [{"name": "Chill Vibes", "tracks": ["a", "b"]}]
    result = pgs.find_playlist_for_mood("sad", playlists)
    assert result is None


@pytest.mark.parametrize(
    "input_time,expected",
    [
        ("2023-01-01 00:00:00", "morning"),
        ("2023-01-01 05:30:00", "morning"),
        ("2023-01-01 13:59:00", "afternoon"),
        ("2023-01-01 18:59:00", "evening"),
        ("2023-01-01 23:00:00", "night"),
        ("05:59", "morning"),
        ("12:00", "afternoon"),
        ("17:00", "evening"),
        ("23:59", "night"),
    ],
)
def test_normalize_time_valid(input_time, expected):
    assert pgs.normalize_time(input_time) == expected


def test_normalize_time_none():
    with pytest.raises(ValueError):
        pgs.normalize_time(None)


def test_normalize_time_invalid_format():
    with pytest.raises(ValueError):
        pgs.normalize_time("not-a-time")


@patch("api.services.playlist_generator_service.get_tracks_by_mood")
def test_extend_playlist_with_tracks(mock_get_tracks):
    playlist = ["a", "b"]
    mock_get_tracks.return_value = ["c", "d"]
    pgs.extend_playlist_with_tracks(4, "happy", playlist)
    assert playlist == ["a", "b", "c", "d"]
    mock_get_tracks.assert_called_once_with("happy", limit=2)


@patch("api.services.playlist_generator_service.infer_mood")
@patch("api.services.playlist_generator_service.load_spotify_playlists")
@patch("api.services.playlist_generator_service.find_playlist_for_mood")
@patch("api.services.playlist_generator_service.extend_playlist_with_tracks")
def test_generate_mood_playlist_local(mock_extend, mock_find, mock_load, mock_infer):
    mock_infer.return_value = "happy"
    mock_load.return_value = [{"name": "Happy", "tracks": ["a", "b", "c"]}]
    mock_find.return_value = ["a", "b", "c"]
    result = pgs.generate_mood_playlist(time_of_day="2023-01-01 05:00:00", max_tracks=2)
    assert result["mood"] == "happy"
    assert result["playlist"] == ["a", "b"]
    assert result["source"] == "local"
    mock_extend.assert_not_called()


@patch("api.services.playlist_generator_service.infer_mood")
@patch("api.services.playlist_generator_service.load_spotify_playlists")
@patch("api.services.playlist_generator_service.find_playlist_for_mood")
@patch("api.services.playlist_generator_service.extend_playlist_with_tracks")
def test_generate_mood_playlist_local_plus_lastfm(
    mock_extend, mock_find, mock_load, mock_infer
):
    mock_infer.return_value = "happy"
    mock_load.return_value = [{"name": "Happy", "tracks": ["a"]}]
    mock_find.return_value = ["a"]

    def extend(max_tracks, mood, playlist):
        playlist.extend(["b", "c"])

    mock_extend.side_effect = extend
    result = pgs.generate_mood_playlist(time_of_day="2023-01-01 05:00:00", max_tracks=3)
    assert result["mood"] == "happy"
    assert result["playlist"] == ["a", "b", "c"]
    assert result["source"] == "local+lastfm"


@patch("api.services.playlist_generator_service.infer_mood")
@patch("api.services.playlist_generator_service.load_spotify_playlists")
@patch("api.services.playlist_generator_service.find_playlist_for_mood")
@patch("api.services.playlist_generator_service.get_tracks_by_mood")
def test_generate_mood_playlist_lastfm(
    mock_get_tracks, mock_find, mock_load, mock_infer
):
    mock_infer.return_value = "sad"
    mock_load.return_value = []
    mock_find.return_value = None
    mock_get_tracks.return_value = ["x", "y"]
    result = pgs.generate_mood_playlist(time_of_day="2023-01-01 23:00:00", max_tracks=2)
    assert result["mood"] == "sad"
    assert result["playlist"] == ["x", "y"]
    assert result["source"] == "lastfm"
    mock_get_tracks.assert_called_once_with("sad", limit=2)
