from twitter_api.error import TwitterApiException
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class TwitterApiWarning(TwitterApiException):
    ...


class RateLimitOverWarning(TwitterApiWarning):
    def __init__(self, rate_limit: RateLimitInfo) -> None:
        self._rate_limit = rate_limit

    def __str__(self) -> str:
        return f"レートリミットを超えています。{self._rate_limit}"


class UnmanagedRateLimitOverWarning(TwitterApiWarning):
    def __str__(self) -> str:
        return f"管理していないレートリミットに遭遇しました。"
