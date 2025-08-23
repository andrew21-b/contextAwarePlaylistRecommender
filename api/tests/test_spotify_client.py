import pytest
from unittest.mock import patch, MagicMock
from api.services.spotify_client import SpotifyClient


@patch("api.services.spotify_client.requests.post")
def test_authenticate_sets_access_token(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "fake_token"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    client = SpotifyClient()

    assert client.access_token == "fake_token"


@patch("api.services.spotify_client.requests.post")
def test_authenticate_raises_error_on_failure(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "invalid_grant"}
    mock_response.raise_for_status.side_effect = Exception("Authentication failed")
    mock_post.return_value = mock_response

    with pytest.raises(Exception, match="Authentication failed"):
        SpotifyClient()


@patch("api.services.spotify_client.requests.get")
@patch("api.services.spotify_client.requests.post")
def test_search_track_success(mock_post, mock_get):
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.raise_for_status.return_value = None
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {
        "tracks": {"items": [{"id": "123", "name": "Test Track"}]}
    }
    mock_get.return_value = mock_get_response

    client = SpotifyClient()
    result = client.search_track("Test Query")
    assert result == {"id": "123", "name": "Test Track"}


@patch("api.services.spotify_client.requests.get")
@patch("api.services.spotify_client.requests.post")
def test_search_track_no_results(mock_post, mock_get):
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.raise_for_status.return_value = None
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"tracks": {"items": []}}
    mock_get.return_value = mock_get_response

    client = SpotifyClient()
    result = client.search_track("No Results Query")
    assert result is None


@patch("api.services.spotify_client.requests.get")
@patch("api.services.spotify_client.requests.post")
def test_search_track_api_error(mock_post, mock_get):

    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.raise_for_status.return_value = None
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.status_code = 400
    mock_get_response.json.return_value = {"tracks": {"items": []}}
    mock_get.return_value = mock_get_response

    client = SpotifyClient()
    result = client.search_track("Error Query")
    assert result is None


@patch("api.services.spotify_client.requests.get")
@patch("api.services.spotify_client.requests.post")
def test_audio_features_success(mock_post, mock_get):
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.raise_for_status.return_value = None
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.raise_for_status.return_value = None
    mock_get_response.json.return_value = {
        "audio_features": [{"id": "1", "danceability": 0.5}]
    }
    mock_get.return_value = mock_get_response

    client = SpotifyClient()
    result = client.audio_features(["1"])
    assert result == [{"id": "1", "danceability": 0.5}]


@patch("api.services.spotify_client.requests.get")
@patch("api.services.spotify_client.requests.post")
def test_audio_features_raises_on_error(mock_post, mock_get):
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.raise_for_status.return_value = None
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.raise_for_status.side_effect = Exception("API error")
    mock_get.return_value = mock_get_response

    client = SpotifyClient()
    with pytest.raises(Exception, match="API error"):
        client.audio_features(["1"])
