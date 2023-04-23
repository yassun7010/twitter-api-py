from abc import ABCMeta, abstractmethod

from twitter_api.types.oauth import CallbackUrl


class TwitterOAuth2Session(metaclass=ABCMeta):
    @abstractmethod
    def generate_authorization_url(self):
        # NOTE: 本来実装は不要だが、モジュールの循環読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth2.oauth2_authorization import (
            OAuth2Authorization,
        )

        return OAuth2Authorization(**{})

    @abstractmethod
    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
        state: str,
        code_verifier: str,
    ):
        # NOTE: 本来実装は不要だが、モジュールの循環読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.api.types.oauth2.oauth2_access_token import OAuth2AccessToken

        return OAuth2AccessToken(**{})

    @abstractmethod
    def generate_client(self, access_token: str):
        # NOTE: 本来実装は不要だが、モジュールの循環読み込みを防ぐため、
        #       偽のデータを作っている。
        from twitter_api.client.twitter_api_client import TwitterApiClient

        return TwitterApiClient.from_oauth2_bearer_token(**{})
