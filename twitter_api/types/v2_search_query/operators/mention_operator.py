from twitter_api.types.v2_user.username import Username

from ._markable_operator import MarkableOperator
from .operator import InvertibleOperator, StandaloneOperator


class MentionOperator(
    MarkableOperator,
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, username: Username):
        super().__init__(username, "@")
