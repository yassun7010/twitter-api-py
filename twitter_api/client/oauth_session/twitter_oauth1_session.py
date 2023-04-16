from abc import ABCMeta, abstractmethod

from twitter_api.api.types.oauth1.oauth1_request_url import OAuth1RequestUrl
from twitter_api.types.oauth import AccessSecret, AccessToken, CallbackUrl


class TwitterOAuth1Session(metaclass=ABCMeta):
    @abstractmethod
    def request_token(self):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth1.twitter_oauth1_authorization_client import (
            TwitterOAuth1AuthorizeClient,
        )

        return TwitterOAuth1AuthorizeClient(**{})

    @abstractmethod
    def generate_authorization_url(
        self,
        url: OAuth1RequestUrl,
    ):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth1.oauth1_authorization import (
            OAuth1Authorization,
        )

        return OAuth1Authorization(**{})

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
    ):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken

        return OAuth1AccessToken(**{})

    @abstractmethod
    def generate_client(self, access_token: AccessToken, access_secret: AccessSecret):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.client.twitter_api_client import TwitterApiClient

        return TwitterApiClient.from_oauth1_app(**{})
