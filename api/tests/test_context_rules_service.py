import pytest
from api.services.context_rules_service import pick_playlist


@pytest.fixture
def playlists():
    return [
        {"name": "Focus", "id": 1},
        {"name": "Late Night", "id": 2},
        {"name": "Commute", "id": 3},
    ]


def test_pick_playlist_focus_on_work_event(playlists):
    context = {"calendar_event": "Work meeting", "time_of_day": "morning"}
    result = pick_playlist(context, playlists)
    assert result["name"] == "Focus"


def test_pick_playlist_focus_on_meeting_event(playlists):
    context = {"calendar_event": "Team Meeting", "time_of_day": "afternoon"}
    result = pick_playlist(context, playlists)
    assert result["name"] == "Focus"


def test_pick_playlist_late_night(playlists):
    context = {"calendar_event": "Party", "time_of_day": "Night"}
    result = pick_playlist(context, playlists)
    assert result["name"] == "Late Night"


def test_pick_playlist_commute_default(playlists):
    context = {"calendar_event": "Lunch", "time_of_day": "morning"}
    result = pick_playlist(context, playlists)
    assert result["name"] == "Commute"


def test_pick_playlist_case_insensitivity(playlists):
    context = {"calendar_event": "WORK", "time_of_day": "NIGHT"}
    result = pick_playlist(context, playlists)
    assert result["name"] == "Focus"
