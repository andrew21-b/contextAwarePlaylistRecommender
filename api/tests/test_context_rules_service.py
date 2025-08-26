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
    context = {"event": "Work meeting", "time_of_day": "morning"}
    result = pick_playlist(context, playlists)
    assert result == "Focus"


def test_pick_playlist_focus_on_meeting_event(playlists):
    context = {"event": "Team Meeting", "time_of_day": "afternoon"}
    result = pick_playlist(context, playlists)
    assert result == "Focus"


def test_pick_playlist_late_night(playlists):
    context = {"event": "Party", "time_of_day": "Night"}
    result = pick_playlist(context, playlists)
    assert result == "Late Night"


def test_pick_playlist_commute_default(playlists):
    context = {"event": "Lunch", "time_of_day": "morning"}
    result = pick_playlist(context, playlists)
    assert result == "Commute"


def test_pick_playlist_case_insensitivity(playlists):
    context = {"event": "WORK", "time_of_day": "NIGHT"}
    result = pick_playlist(context, playlists)
    assert result == "Focus"
