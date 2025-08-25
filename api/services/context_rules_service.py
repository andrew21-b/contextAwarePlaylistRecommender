def pick_playlist(context, playlists):
    event = context["event"].lower()
    time_of_day = context["time_of_day"].lower()

    if "work" in event or "meeting" in event:
        return next(playlist for playlist in playlists if playlist["name"] == "Focus")
    elif "night" in time_of_day:
        return next(
            playlist for playlist in playlists if playlist["name"] == "Late Night"
        )
    else:
        return next(playlist for playlist in playlists if playlist["name"] == "Commute")
