from datetime import datetime


def safe_isoformat(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.isoformat()
