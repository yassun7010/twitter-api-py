from ._specific_keyword import SpecificKeyword
from .operator import Operator


class Hashtag(SpecificKeyword, Operator):
    def __init__(self, hashtag: str):
        super().__init__(hashtag, "#")
