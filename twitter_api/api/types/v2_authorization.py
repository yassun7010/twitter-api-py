from dataclasses import dataclass
from textwrap import dedent
from typing import Callable, Literal, Optional, Self

from authlib.integrations.requests_client.oauth2_session import OAuth2Session

from twitter_api.api.resources.oauth2_authorize import Oauth2AuthorizeUrl
from twitter_api.api.resources.oauth2_authorize.get_oauth2_authorize import ENDPOINT
from twitter_api.api.types.v2_scope import Scope
from twitter_api.rate_limit.manager.rate_limit_manager import RateLimitManager
from twitter_api.types.comma_separatable import CommaSeparatable
from twitter_api.types.http import Url
from twitter_api.types.oauth import AccessToken, ClientId, ClientSecret
from twitter_api.utils.oauth import generate_code_verifier

V2Oauth2TokenUrl = Literal["https://api.twitter.com/2/oauth2/token"]


@dataclass
class OAuthV2AcccessToken:
    token_type: Literal["bearer"]
    expires_in: int
    expires_at: int
    access_token: AccessToken
    scope: CommaSeparatable[Scope]

    def generate_client(self):
        from twitter_api.client.twitter_api_real_client import TwitterApiRealClient

        return TwitterApiRealClient.from_app_oauth2_bearer_token(self.access_token)


@dataclass
class OpenOAuthV2AccessTokenResource:
    client_id: ClientId
    client_secret: ClientSecret
    url: V2Oauth2TokenUrl
    authorization_response_url: str
    state: Optional[str]
    code_verifier: str
    _session: OAuth2Session

    def post(self) -> OAuthV2AcccessToken:
        return OAuthV2AcccessToken(
            **self._session.fetch_token(
                url=self.url,
                authorization_response=self.authorization_response_url,
                state=self.state,
                code_verifier=self.code_verifier,
            )
        )


@dataclass
class OpenOAuthV2AuthorizationResponseResource:
    client_id: ClientId
    client_secret: ClientSecret
    authorization_response_url: Url
    state: str
    code_verifier: str
    _session: OAuth2Session

    def request(self, url: V2Oauth2TokenUrl):
        return OpenOAuthV2AccessTokenResource(
            url=url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_response_url=self.authorization_response_url,
            state=None,
            code_verifier=self.code_verifier,
            _session=self._session,
        )


@dataclass
class OpenOAuthV2AuthorizationResource:
    client_id: ClientId
    client_secret: ClientSecret
    authorization_url: Url
    state: str
    code_verifier: str
    _session: OAuth2Session

    def open_authorization_url(self) -> Self:
        import webbrowser

        webbrowser.open(self.authorization_url)
        return self

    def print_authorization_url(
        self, message_function: Optional[Callable[[Url], str]] = None
    ) -> Self:
        if message_function is None:

            def default_message_function(url: Url):
                return dedent(
                    f"""
                    Please open Authorization URL using your browser.
                        {url}
                    """
                )

            message_function = default_message_function

        print(message_function(self.authorization_url))
        return self

    def input_authorization_response_url(
        self,
        input_url: Optional[Url] = None,
    ):
        if input_url is None:
            input_url = ""
        while True:
            if input_url != "":
                break

            input_url = input(
                "Please Authorization Response URL: ",
            )

        return OpenOAuthV2AuthorizationResponseResource(
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_response_url=input_url,
            state=self.state,
            code_verifier=self.code_verifier,
            _session=self._session,
        )


@dataclass
class OAuthV2AuthorizeData:
    client_id: ClientId
    client_secret: ClientSecret
    callback_url: Url
    scope: CommaSeparatable[Scope]
    rate_limit_manager: Optional[RateLimitManager] = None

    def chain(self) -> Self:
        return self

    def request(self, url: Oauth2AuthorizeUrl) -> OpenOAuthV2AuthorizationResource:
        session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.callback_url,
            scope=self.scope,
            code_challenge_method="S256",
        )

        code_verifier = generate_code_verifier()

        authorization_url, state = session.create_authorization_url(
            ENDPOINT.url, code_verifier=code_verifier
        )
        return OpenOAuthV2AuthorizationResource(
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorization_url=authorization_url,
            state=state,
            code_verifier=code_verifier,
            _session=session,
        )
