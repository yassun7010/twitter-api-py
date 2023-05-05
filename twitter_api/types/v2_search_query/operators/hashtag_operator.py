from twitter_api.types.v2_hashtag import Hashtag

from ._markable_operator import MarkableOperator
from .operator import InvertibleOperator, StandaloneOperator


class HashtagOperator(
    MarkableOperator,
    InvertibleOperator,
    StandaloneOperator,
):
    def __init__(self, hashtag: Hashtag):
        super().__init__(hashtag, "#")
