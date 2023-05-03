from twitter_api.client.oauth_flow.twitter_oauth1_authorization_client import (
    TwitterOAuth1AuthorizeClient,
)
from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth1SessionResources,
)
from twitter_api.types._generic_client import TwitterApiGenericClient


class PostOAuth1RequestTokenSessionResources(
    OAuth1SessionResources[TwitterApiGenericClient]
):
    def post(self) -> TwitterOAuth1AuthorizeClient[TwitterApiGenericClient]:
        """
        OAuth 1.0a の最初のステップ。
        ユーザーアクセストークンのセットを生成するためにリクエストを送信する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/request_token
        """
        return self._session.request_token()
