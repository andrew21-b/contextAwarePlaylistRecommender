import pytest
from unittest.mock import patch, MagicMock
from api.services.lastfm_client import get_similar_tracks


@patch("api.services.lastfm_client.settings")
@patch("api.services.lastfm_client.requests.get")
def test_get_similar_tracks_success(mock_get, mock_settings):
    mock_settings.LASTFM_API_KEY = "dummy_key"
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "similartracks": {
            "track": [
                {"name": "Track1", "artist": {"name": "Artist1"}},
                {"name": "Track2", "artist": {"name": "Artist2"}},
            ]
        }
    }
    mock_get.return_value = mock_response

    result = get_similar_tracks("SomeArtist", "SomeTrack", limit=2)
    assert result == ["Artist1 - Track1", "Artist2 - Track2"]
    mock_get.assert_called_once()

    args, kwargs = mock_get.call_args
    assert kwargs["params"]["artist"] == "SomeArtist"
    assert kwargs["params"]["track"] == "SomeTrack"
    assert kwargs["params"]["limit"] == 2
    assert kwargs["params"]["api_key"] == "dummy_key"


@patch("api.services.lastfm_client.settings")
@patch("api.services.lastfm_client.requests.get")
def test_get_similar_tracks_no_similartracks(mock_get, mock_settings):
    mock_settings.LASTFM_API_KEY = "dummy_key"
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_similar_tracks("Artist", "Track")
    assert result == []


@patch("api.services.lastfm_client.settings")
@patch("api.services.lastfm_client.requests.get")
def test_get_similar_tracks_empty_track_list(mock_get, mock_settings):
    mock_settings.LASTFM_API_KEY = "dummy_key"
    mock_response = MagicMock()
    mock_response.json.return_value = {"similartracks": {"track": []}}
    mock_get.return_value = mock_response

    result = get_similar_tracks("Artist", "Track")
    assert result == []
