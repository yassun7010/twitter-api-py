import sys
from textwrap import dedent
from typing import Callable, Generic, Optional, TextIO

from twitter_api.client.oauth_session.twitter_oauth2_session import TwitterOAuth2Session
from twitter_api.types._generic_client import TwitterApiGenericClient
from twitter_api.types.http import Url


class _OAuth2Authorization(Generic[TwitterApiGenericClient]):
    def __init__(
        self,
        *,
        authorization_url: Url,
        state: str,
        code_verifier: str,
        session: TwitterOAuth2Session[TwitterApiGenericClient],
    ) -> None:
        self.authorization_url = authorization_url
        self.state = state
        self.code_verifier = code_verifier
        self._session = session

    def input_response_url(
        self,
        response_url: Optional[Url] = None,
        *,
        message_function: Optional[Callable[[], str]] = None,
        message_io: TextIO = sys.stderr,
    ):
        """
        Twitter 認証画面で承認した後にリダイレクトされるコールバックURL を入力する。

        引数の response_url に値がない場合、プロンプトで問い合わせを行う。
        """

        from twitter_api.client.oauth_flow.twitter_oauth2_access_token_client import (
            TwitterOAuth2AccessTokenClient,
        )

        if response_url is None:
            response_url = ""

        if message_function is None:

            def default_message_function():
                return "Please input Authorization Response URL: "

            message_function = default_message_function

        while True:
            if response_url != "":
                break

            message_io.write(message_function())
            response_url = input()

        return TwitterOAuth2AccessTokenClient(
            authorization_response_url=response_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )


class OAuth2Authorization(_OAuth2Authorization[TwitterApiGenericClient]):
    def open_request_url(self) -> _OAuth2Authorization[TwitterApiGenericClient]:
        """
        Twitter 認証画面の URL をブラウザで認証画面を開く。
        """
        import webbrowser

        webbrowser.open(self.authorization_url)

        return _OAuth2Authorization(
            authorization_url=self.authorization_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )

    def print_request_url(
        self,
        message_function: Optional[Callable[[Url], str]] = None,
        message_io: TextIO = sys.stderr,
    ) -> _OAuth2Authorization[TwitterApiGenericClient]:
        """
        Twitter 認証画面の URL をコンソール上に出力する。
        """
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

        print(message_function(self.authorization_url), file=message_io)

        return _OAuth2Authorization(
            authorization_url=self.authorization_url,
            state=self.state,
            code_verifier=self.code_verifier,
            session=self._session,
        )
