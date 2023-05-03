from ._markable_operator import MarkableOperator
from .operator import Operator


class CashtagOperator(MarkableOperator[Operator]):
    def __init__(self, cashtag: str):
        super().__init__(cashtag, "$")
