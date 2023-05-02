from twitter_api.error import TwitterApiException
from twitter_api.rate_limit.rate_limit_info import RateLimitInfo


class TwitterApiWarning(TwitterApiException):
    ...


class RateLimitOverWarning(TwitterApiWarning):
    def __init__(self, rate_limit: RateLimitInfo) -> None:
        self._rate_limit = rate_limit

    @property
    def message(self) -> str:
        return f"レートリミットを超えています。{self._rate_limit}"


class UnmanagedRateLimitOverWarning(TwitterApiWarning):
    @property
    def message(self) -> str:
        return "管理していないレートリミットに遭遇しました。"
