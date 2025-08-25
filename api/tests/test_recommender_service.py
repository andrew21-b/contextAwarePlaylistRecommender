import pytest
import random
from unittest.mock import patch
from api.services.recommender_service import recommend_for_context


@pytest.fixture
def playlists():
    return [
        {
            "name": "Chill Vibes",
            "tracks": ["Artist1 - SongA", "Artist2 - SongB", "Artist3 - SongC"],
        },
        {
            "name": "Workout",
            "tracks": ["Artist4 - SongD", "Artist5 - SongE"],
        },
    ]


@patch("api.services.recommender_service.pick_playlist")
@patch("api.services.recommender_service.get_similar_tracks")
@patch("random.choice")
def test_recommend_for_context_returns_expected_structure(
    mock_choice, mock_get_similar_tracks, mock_pick_playlist, playlists
):
    context = "relax"
    base_playlist = playlists[0]
    mock_pick_playlist.return_value = base_playlist
    mock_choice.return_value = "Artist1 - SongA"
    mock_get_similar_tracks.return_value = ["TrackX", "TrackY", "TrackZ"]

    result = recommend_for_context(context, playlists)

    assert result["context"] == context
    assert result["base_playlist"] == base_playlist["name"]
    assert result["seed_track"] == "Artist1 - SongA"
    assert result["recommendations"] == ["TrackX", "TrackY", "TrackZ"]


@patch("api.services.recommender_service.pick_playlist")
@patch("api.services.recommender_service.get_similar_tracks")
@patch("random.choice")
def test_recommend_for_context_calls_dependencies_correctly(
    mock_choice, mock_get_similar_tracks, mock_pick_playlist, playlists
):
    context = "workout"
    base_playlist = playlists[1]
    mock_pick_playlist.return_value = base_playlist
    mock_choice.return_value = "Artist4 - SongD"
    mock_get_similar_tracks.return_value = []

    recommend_for_context(context, playlists)

    mock_pick_playlist.assert_called_once_with(context, playlists)
    mock_choice.assert_called_once_with(base_playlist["tracks"])
    mock_get_similar_tracks.assert_called_once_with("Artist4", "SongD", limit=5)


@patch("api.services.recommender_service.pick_playlist")
@patch("api.services.recommender_service.get_similar_tracks")
@patch("random.choice")
def test_recommend_for_context_handles_multiple_tracks(
    mock_choice, mock_get_similar_tracks, mock_pick_playlist, playlists
):
    context = "chill"
    base_playlist = playlists[0]
    mock_pick_playlist.return_value = base_playlist
    mock_choice.return_value = "Artist2 - SongB"
    mock_get_similar_tracks.return_value = ["Rec1", "Rec2"]

    result = recommend_for_context(context, playlists)

    assert result["seed_track"] == "Artist2 - SongB"
    assert result["recommendations"] == ["Rec1", "Rec2"]
