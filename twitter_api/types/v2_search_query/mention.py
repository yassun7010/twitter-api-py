from twitter_api.types.v2_user.username import Username

from .operator import Operator


class Mention(Operator):
    def __init__(self, username: Username):
        self._username = username[1:] if username.startswith("@") else username

    def __str__(self) -> str:
        return f"@{self._username}"
