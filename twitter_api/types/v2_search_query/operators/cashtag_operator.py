from twitter_api.types.v2_cashtag import Cashtag

from ._markable_operator import MarkableOperator
from .operator import Operator


class CashtagOperator(MarkableOperator[Operator]):
    def __init__(self, cashtag: Cashtag):
        super().__init__(cashtag, "$")
