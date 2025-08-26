def is_context_valid(context):
    if context["event"] != None or context["time_of_day"] != None:
        return True
    return False


def pick_playlist(context, playlists) -> str:
    if not is_context_valid(context):
        return playlists[1][0]

    event = context["event"].lower() if context["event"] else ""
    time_of_day = context["time_of_day"].lower() if context["time_of_day"] else ""

    if "work" in event or "meeting" in event:
        return "Focus"
    elif "night" in time_of_day:
        return "Late Night"
    else:
        return "Commute"
