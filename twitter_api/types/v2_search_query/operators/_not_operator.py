from .operator import Operator, WeakOperator


class NotOperator(
    # NOTE: 否定は CorrectOperator ではなく、 WeakOperator である。
    #       言い換えれば、否定だけの条件による検索を禁止している。
    #       そうでないクエリを作成することはできるだろうが、検索効率の悪いクエリになる。
    #       本ツールでは、意図的に否定から開始するクエリを禁止する。
    WeakOperator,
):
    def __init__(self, op: Operator) -> None:
        self._op = op

    def __str__(self) -> str:
        return f"-{self._op}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._op)})"
