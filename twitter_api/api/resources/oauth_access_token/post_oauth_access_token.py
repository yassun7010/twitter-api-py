from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.oauth import CallbackUrl


class PostOauthAccessTokenResources:
    def __init__(
        self,
        authorization_response_url: CallbackUrl,
        session: TwitterOAuth1Session,
    ) -> None:
        self._authorization_response_url = authorization_response_url
        self._session = session

    def post(
        self,
    ) -> OAuth1AccessToken:
        """
        OAuth 1.0a の最後のステップ。
        ユーザーアクセストークンのセットを生成するために使用する。

        refer: https://developer.twitter.com/en/docs/authentication/api-reference/access_token
        """

        return self._session.fetch_token(self._authorization_response_url)


class AsyncPostOauthAccessTokenResources(PostOauthAccessTokenResources):
    async def post(self) -> OAuth1AccessToken:
        return super().post()
