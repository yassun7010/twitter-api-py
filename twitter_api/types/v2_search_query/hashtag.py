from twitter_api.types.v2_search_query.operator import Operator


class Hashtag(Operator):
    def __init__(self, hashtag: str):
        self._hashtag = hashtag[1:] if hashtag.startswith("#") else hashtag

    def __str__(self) -> str:
        return f"#{self._hashtag}"
