from twitter_api.client.oauth_flow.twitter_oauth1_authorization_client import (
    TwitterOAuth1AuthorizeClient,
)
from twitter_api.client.oauth_session.resources.oauth1_authenticate import (
    OauthAuth1enticateUrl,
)
from twitter_api.client.oauth_session.resources.oauth1_authorize import (
    Oauth1AuthorizeUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.oauth import AccessSecret, AccessToken, CallbackUrl


class TwitterOAuth1MockSession(TwitterOAuth1Session):
    def request_token(self) -> TwitterOAuth1AuthorizeClient:
        return TwitterOAuth1AuthorizeClient(session=self)

    def generate_authorization_url(
        self,
        url: OauthAuth1enticateUrl | Oauth1AuthorizeUrl,
    ):
        from twitter_api.api.types.oauth1.oauth1_authorization import (
            OAuth1Authorization,
        )

        return OAuth1Authorization(
            authorization_url="https://authorization.url.com",
            session=self,
        )

    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
    ):
        from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken

        return OAuth1AccessToken(
            oauth_token="oauth_token",
            oauth_token_secret="oauth_token_secret",
            user_id="user_id",
            screen_name="screen_name",
            _session=self,
        )

    def generate_client(self, access_token: AccessToken, access_secret: AccessSecret):
        from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient

        return TwitterApiMockClient.from_oauth1_app(
            api_key="api_key",
            api_secret="api_secret",
            access_token=access_token,
            access_secret=access_secret,
        )
