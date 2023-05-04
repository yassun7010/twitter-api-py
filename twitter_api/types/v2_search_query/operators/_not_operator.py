from .group_operator import grouping
from .operator import Operator


class NotOperator(
    # NOTE: 否定は CorrectOperator ではない。
    #       言い換えれば、クエリの最初、またはグループの最初は否定以外から開始しなければならない。
    #       そうでないクエリを作成することはできるだろうが、検索効率の悪いクエリになる。
    #       本ツールでは、意図的に否定から開始するクエリを禁止する。
    #
    # CorrectOperator[Operator],
    Operator,
):
    def __init__(self, op: Operator) -> None:
        self._op = op

    def __str__(self) -> str:
        return f"-{grouping(self._op)}"
