from twitter_api.types.v2_user.username import Username

from ._markable_operator import MarkableOperator
from .operator import InvertableOperator, Operator, StandaloneOperator


class MentionOperator(
    MarkableOperator,
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, username: Username):
        super().__init__(username, "@")
