from typing import Optional

from authlib.integrations.httpx_client.oauth1_client import OAuth1Client

from twitter_api.api.types.oauth1.oauth1_authorization import OAuth1Authorization
from twitter_api.client.oauth_flow.twitter_oauth1_authorization_client import (
    TwitterOAuth1AuthorizeClient,
)
from twitter_api.client.oauth_session.resources.oauth1_access_token import (
    Oauth1AccessTokenUrl,
)
from twitter_api.client.oauth_session.resources.oauth1_authenticate import (
    OauthAuth1enticateUrl,
)
from twitter_api.client.oauth_session.resources.oauth1_authorize import (
    Oauth1AuthorizeUrl,
)
from twitter_api.client.oauth_session.resources.oauth1_request_token import (
    Oauth1RequestTokenUrl,
)
from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types.oauth import (
    AccessSecret,
    AccessToken,
    ApiKey,
    ApiSecret,
    CallbackUrl,
)


class TwitterOAuth1RealSession(TwitterOAuth1Session):
    def __init__(
        self,
        *,
        api_key: ApiKey,
        api_secret: ApiSecret,
        callback_url: CallbackUrl,
        rate_limit_manager: Optional[RateLimitManager] = None,
    ) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._session = OAuth1Client(
            client_id=api_key,
            client_secret=api_secret,
            redirect_uri=callback_url,
        )
        self._rate_limit_manager = rate_limit_manager

    def request_token(self) -> TwitterOAuth1AuthorizeClient:
        url: Oauth1RequestTokenUrl = "https://api.twitter.com/oauth/request_token"

        self._session.fetch_request_token(url)

        return TwitterOAuth1AuthorizeClient(session=self)

    def generate_authorization_url(
        self,
        url: OauthAuth1enticateUrl | Oauth1AuthorizeUrl,
    ) -> OAuth1Authorization:
        return OAuth1Authorization(
            authorization_url=self._session.create_authorization_url(url),
            session=self,
        )

    def fetch_token(
        self,
        authorization_response_url: CallbackUrl,
    ):
        from twitter_api.api.types.oauth1.oauth1_access_token import OAuth1AccessToken

        url: Oauth1AccessTokenUrl = "https://api.twitter.com/oauth/access_token"

        self._session.parse_authorization_response(authorization_response_url)

        data = self._session.fetch_access_token(url=url)

        return OAuth1AccessToken(
            oauth_token=data["oauth_token"],
            oauth_token_secret=data["oauth_token_secret"],
            user_id=data["user_id"],
            screen_name=data["screen_name"],
            _session=self,
        )

    def generate_client(self, access_token: AccessToken, access_secret: AccessSecret):
        from twitter_api.client.twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_oauth1_app(
            api_key=self._api_key,
            api_secret=self._api_secret,
            access_token=access_token,
            access_secret=access_secret,
            rate_limit_manager=self._rate_limit_manager,
        )
