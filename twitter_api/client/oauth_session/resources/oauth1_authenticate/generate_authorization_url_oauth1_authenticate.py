from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth1SessionResources,
)
from twitter_api.types._generic_client import TwitterApiGenericClient


class GenerateAuthorizationUrlOAuth1AuthenticateSessionResources(
    OAuth1SessionResources[TwitterApiGenericClient]
):
    def generate_authorization_url(self):
        """
        OAuth 1.0a の 2 番目のステップ。
        ユーザーアクセストークンのセットを生成するために、
        Twitter 認証画面へのアクセス用 URL を生成する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authenticate
        """

        return self._session.generate_authorization_url(
            "https://api.twitter.com/oauth/authenticate",
        )
