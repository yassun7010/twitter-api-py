import sys
from textwrap import dedent
from typing import Callable, Optional, Self, TextIO

from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types.chainable import Chainable
from twitter_api.types.http import Url


class OAuth2Authorization(Chainable):
    def __init__(
        self,
        authorization_url: Url,
        state: str,
        code_verifier: str,
        session: TwitterOAuth2Session,
    ) -> None:
        self.authorization_url = authorization_url
        self.state = state
        self.code_verifier = code_verifier
        self._session = session

    def open_request_url(self) -> Self:
        import webbrowser

        webbrowser.open(self.authorization_url)
        return self

    def print_request_url(
        self,
        message_function: Optional[Callable[[Url], str]] = None,
        file: TextIO = sys.stderr,
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

        print(message_function(self.authorization_url), file=file)

        return self

    def input_response_url(
        self,
        input_url: Optional[Url] = None,
        *,
        message_function: Optional[Callable[[], str]] = None,
        file: TextIO = sys.stderr,
    ):
        """
        認証画面で承認した後にリダイレクトされるコールバックURL を入力する。

        引数の input_url に値を入れると、プロンプトで問い合わせを行わない。
        """

        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_client import (
            TwitterOAuth2AccessTokenClient,
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

            file.write(message_function())
            input_url = input()

        return TwitterOAuth2AccessTokenClient(
            authorization_response_url=input_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )
