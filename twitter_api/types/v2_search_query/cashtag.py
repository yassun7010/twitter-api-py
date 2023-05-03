from ._specific_keyword import SpecificKeyword
from .operator import Operator


class Cashtag(SpecificKeyword, Operator[Operator]):
    def __init__(self, cashtag: str):
        super().__init__(cashtag, "$")
