from twitter_api.types.v2_entity.entity_name import EntityName

from .operator import InvertableOperator, Operator, StandaloneOperator


class EntityOperator(
    InvertableOperator[Operator],
    StandaloneOperator[Operator],
):
    def __init__(self, name: EntityName):
        self._value = name

    def __str__(self) -> str:
        return f'entity:"{self._value}"'
