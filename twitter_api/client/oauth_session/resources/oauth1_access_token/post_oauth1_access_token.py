from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken
from twitter_api.client.oauth_session.resources.session_resources import (
    OAuth1SessionResources,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.oauth import CallbackUrl


class PostOauth1AccessTokenResources(OAuth1SessionResources):
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        session: TwitterOAuth1Session,
    ) -> None:
        self._authorization_response_url = authorization_response_url
        super().__init__(session)

    def post(
        self,
    ) -> OAuth1AccessToken:
        """
        OAuth 1.0a の最後のステップ。
        ユーザーアクセストークンのセットを生成する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/access_token
        """

        return self._session.fetch_token(self._authorization_response_url)
