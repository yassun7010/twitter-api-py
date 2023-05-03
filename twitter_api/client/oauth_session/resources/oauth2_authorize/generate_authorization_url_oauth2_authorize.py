from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth2SessionResources,
)
from twitter_api.types._generic_client import TwitterApiGenericClient


class GenerateAuthorizationUrlOAuth2AuthorizeSessionResources(
    OAuth2SessionResources[TwitterApiGenericClient],
):
    def generate_authorization_url(self):
        """
        OAuth 2.0 のユーザ認証（PKCE）の最初のステップ。

        ユーザーアクセストークンのセットを生成するために、
        Twitter 認証画面へのアクセス用 URL を生成する。

        refer: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
        """

        return self._session.generate_authorization_url()
