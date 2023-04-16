from twitter_api.api.types.oauth1.oauth1_request_url import OAuth1RequestUrl
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable


class OAuth1GenerateAuthorizationUrlSession(Chainable):
    def __init__(
        self,
        url: OAuth1RequestUrl,
        session: TwitterOAuth1Session,
    ):
        self._url: OAuth1RequestUrl = url
        self._session = session

    def generate_authorization_url(self):
        """
        OAuth 1.0a の 2 番目のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/authorize
        """

        return self._session.generate_authorization_url(self._url)
