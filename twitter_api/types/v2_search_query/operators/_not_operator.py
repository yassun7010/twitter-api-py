from .operator import IncompleteOperator, Operator


class NotOperator(
    # NOTE: 否定は CompleteOperator ではなく、 IncompleteOperator である。
    #       公式ドキュメント上でも、否定だけの条件による検索を禁止されている。
    IncompleteOperator,
):
    def __init__(self, op: Operator) -> None:
        self._op = op

    def __str__(self) -> str:
        return f"-{self._op}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._op)})"
