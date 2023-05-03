from twitter_api.types.v2_search_query.operator import Operator


class Cashtag(Operator):
    def __init__(self, cashtag: str):
        self._cashtag = cashtag[1:] if cashtag.startswith("$") else cashtag

    def __str__(self) -> str:
        return f"${self._cashtag}"
