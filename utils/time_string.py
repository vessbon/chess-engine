def get_time_string(total_seconds: float) -> str:
    """Formats the internal float seconds into a clean UI string."""
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    tenths = int((total_seconds % 1) * 10)

    if total_seconds < 10 and total_seconds > 0:
        return f"{seconds:02d}.{tenths}"

    return f"{minutes:02d}:{seconds:02d}"
