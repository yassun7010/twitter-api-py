from typing import Any, Optional, overload

null = None
"""Json のデータをそのままコードにコピーして利用できるように、 null を定義しておく。"""

true = True
"""Json のデータをそのままコードにコピーして利用できるように、 true を定義しておく。"""

false = False
"""Json のデータをそのままコードにコピーして利用できるように、 false を定義しておく。"""


@overload
def exclude_none(data: dict) -> dict:
    ...


@overload
def exclude_none(data: Optional[dict]) -> Optional[dict]:
    ...


def exclude_none(data: Optional[dict]) -> Optional[dict]:
    if data is None:
        return None

    return {k: _exclude_none_recursive(v) for k, v in data.items() if v is not None}


def _exclude_none_recursive(data: Any):
    if isinstance(data, dict):
        return exclude_none(data)
    else:
        return data


__all__ = ["null", "true", "false"]
