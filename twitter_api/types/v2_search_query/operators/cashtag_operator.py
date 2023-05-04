from twitter_api.types.v2_cashtag import Cashtag

from ._markable_operator import MarkableOperator
from .operator import InvertableOperator, Operator, StandaloneOperator


class CashtagOperator(
    MarkableOperator,
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, cashtag: Cashtag):
        super().__init__(cashtag, "$")
