from twitter_api.rate_limit.manager.no_operation_rate_limit_manager import (
    NoOperationRateLimitManager,
)

DEFAULT_RATE_LIMIT_MANAGER = NoOperationRateLimitManager()
"""
デフォルトのレートリミットマネージャ。

NoOperationRateLimitManager は状態を持たない実装のため、
関数の引数のデフォルト値として与えても問題のないマネージャである。

NOTE: Python のデフォルト値の扱い上、状態を持つマネージャは
      関数定義上のデフォルト値にすることはできないことに注意が必要である。
"""
