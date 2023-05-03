from ._markable_operator import MarkableOperator
from .operator import Operator


class HashtagOperator(MarkableOperator[Operator]):
    def __init__(self, hashtag: str):
        super().__init__(hashtag, "#")
