from typing import Optional, TypeAlias, TypeVar, Union

T = TypeVar("T", bound=str)

CommaSeparatedStr: TypeAlias = str
"""
要素がカンマ区切りで結合された文字列。
"""

CommaSeparatable = Union[T, list[T]]
"""
カンマ区切りとして表現可能な文字列。

Python 上ではカンマ区切りの文字列としても、文字列の配列としても扱える。
"""


def comma_separated_str(
    data: Optional[CommaSeparatable[T]],
) -> Optional[CommaSeparatedStr]:
    """
    カンマ区切りの文字列に変換する。
    """

    if data is None:
        return None

    if isinstance(data, list):
        return ",".join(data)
    else:
        return data
