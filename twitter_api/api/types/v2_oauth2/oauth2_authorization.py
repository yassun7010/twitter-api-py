from dataclasses import dataclass
from textwrap import dedent
from typing import Callable, Optional, Self

from authlib.integrations.requests_client.oauth2_session import OAuth2Session

from twitter_api.types.chainable import Chainable
from twitter_api.types.http import Url


@dataclass
class OAuth2Authorization(Chainable):
    authorization_url: Url
    state: str
    code_verifier: str
    _session: OAuth2Session

    def open_request_url(self) -> Self:
        import webbrowser

        webbrowser.open(self.authorization_url)
        return self

    def print_request_url(
        self, message_function: Optional[Callable[[Url], str]] = None
    ) -> Self:
        if message_function is None:

            def default_message_function(url: Url):
                return dedent(
                    f"""
                    =====================================================
                      Please open Authorization URL using your browser.
                    =====================================================

                        {url}
                    """
                )

            message_function = default_message_function

        print(message_function(self.authorization_url))

        return self

    def input_response_url(
        self,
        input_url: Optional[Url] = None,
    ):
        from twitter_api.api.types.v2_oauth2.twitter_oauth2_access_token_client import (
            TwitterOAuth2AccessTokenClient,
        )

        if input_url is None:
            input_url = ""
        while True:
            if input_url != "":
                break

            input_url = input(
                "Please input Authorization Response URL: ",
            )

        return TwitterOAuth2AccessTokenClient(
            authorization_response_url=input_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )
