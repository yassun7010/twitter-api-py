from abc import ABCMeta, abstractmethod

from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken
from twitter_api.client.twitter_api_client import TwitterApiClient
from twitter_api.types.oauth import AccessSecret, AccessToken, CallbackUrl


class TwitterOAuth1Session(metaclass=ABCMeta):
    @abstractmethod
    def request_token(self):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth1.twitter_oauth1_authorization_client import (
            TwitterOAuth1AuthorizeClient,
        )

        return TwitterOAuth1AuthorizeClient(session=self)

    @abstractmethod
    def generate_authorization_url(self):
        # NOTE: 本来実装は不要だが、モジュールの再起読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth1.oauth1_authorization import (
            OAuth1Authorization,
        )

        return OAuth1Authorization(
            authorization_url="dummy",
            session=self,
        )

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
    ) -> OAuth1AccessToken:
        ...
