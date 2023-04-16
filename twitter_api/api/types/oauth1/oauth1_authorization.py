from textwrap import dedent
from typing import Callable, Optional, Self

from twitter_api.client.oauth_session.twitter_oauth1_session import TwitterOAuth1Session
from twitter_api.types.chainable import Chainable
from twitter_api.types.http import Url


class OAuth1Authorization(Chainable):
    def __init__(
        self,
        authorization_url: Url,
        session: TwitterOAuth1Session,
    ) -> None:
        self.authorization_url = authorization_url
        self._session = session

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
        *,
        message_function: Optional[Callable[[], str]] = None,
    ):
        from twitter_api.api.types.oauth1.twitter_oauth1_access_token_client import (
            TwitterOAuth1AccessTokenClient,
        )

        if input_url is None:
            input_url = ""

        if message_function is None:

            def default_message_function():
                return "Please input Authorization Response URL: "

            message_function = default_message_function

        while True:
            if input_url != "":
                break

            input_url = input(message_function())

        return TwitterOAuth1AccessTokenClient(
            authorization_response_url=input_url,
            session=self._session,
        )
