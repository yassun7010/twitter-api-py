from datetime import datetime


def rfc3339(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
