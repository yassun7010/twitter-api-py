"""
JSON のデータをそのまま Python のコードとして使えるようにするための定数定義。

>>> from twitter_api.utils.json import *
>>> {"a": null, "b": 1, "c": "2", "d": true, "e": false, "f": [3, 4], "g": {"h": 5}}
{'a': None, 'b': 1, 'c': '2', 'd': True, 'e': False, 'f': [3, 4], 'g': {'h': 5}}
"""

null = None
"""Json のデータをそのままコードにコピーして利用できるように、 null を定義しておく。"""

true = True
"""Json のデータをそのままコードにコピーして利用できるように、 true を定義しておく。"""

false = False
"""Json のデータをそのままコードにコピーして利用できるように、 false を定義しておく。"""


__all__ = ["null", "true", "false"]
